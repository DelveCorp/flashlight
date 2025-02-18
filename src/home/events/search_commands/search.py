import argparse
from datetime import (
    timedelta,
)
import operator
import logging
from itertools import groupby

from dateutil import parser as date_parser

from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.module_loading import import_string
from django.forms.models import model_to_dict
from django.contrib.auth.models import Permission

from events.validators import MustBeFirst
from events.util import resolve


# from events.models import Event
# from events.serializers import (
#     EventSerializer,
# )

from .util import cast
from .decorators import search_command

from django.db.models import F, Q

def dict_search(request, events, args):
    raise NotImplementedError("Search must appear as the first search command.")

def orm_search(request, events, args):
    log = logging.getLogger(__name__)
    search_filters = []
    search_excludes = []
    if args.terms:
        for kv_pair in args.terms:
            log.info(f"Received kv_pair: {kv_pair}")
            key, value = kv_pair.split("=", 1)
            value = cast(value)
            if key.startswith("!"):
                key = key.lstrip("!")
                search_excludes.append(Q(**{key: value}))
            else:
                search_filters.append(Q(**{key: value}))
    # search_filters["user"] = request.user.id
    model = import_string(args.model)

    # Now check that the current user has view permission for the model
    permission_names = [
        f"{model._meta.app_label}.{perm.codename}" for perm in
        Permission.objects.filter(
            content_type__model=model._meta.model_name
        )
        if "view" in perm.codename
    ]
    if len(permission_names) > 1:
        raise ValueError(f"Ambiguous permissions found: {permission_names}")
    elif len(permission_names) < 1:
        raise ValueError(f"No view permissions found for {model}")
    else:
        if not request.user.has_perm(permission_names[0]):
            raise PermissionError(f"You do not have permission to access model {model._meta.model_name}")

    ret = model.objects.all()
    for search_filter in search_filters:
        ret = ret.filter(search_filter)
    for search_exclude in search_excludes:
        ret = ret.exclude(search_exclude)

    if args.last_15_minutes:
        ret = ret.filter(
            created__gte=timezone.now() - timedelta(minutes=15)
        )
    elif args.last_hour:
        ret = ret.filter(
            created__gte=timezone.now() - timedelta(hours=1)
        )
    elif args.last_day:
        ret = ret.filter(
            created__gte=timezone.now() - timedelta(days=1)
        )
    elif args.last_week:
        ret = ret.filter(
            created__gte=timezone.now() - timedelta(weeks=1)
        )
    elif args.last_month:
        ret = ret.filter(
            created__gte=timezone.now() - timedelta(months=1)
        )
    if args.older_than:
        older_than = date_parser.parse(args.older_than)
        log.info(f"Found older_than: {type(older_than)}({older_than})")
        ret = ret.filter(
            created__lt=older_than,
        )
    if args.newer_than:
        newer_than = date_parser.parse(args.newer_than)
        log.info(f"Found newer_than: {type(newer_than)}({newer_than})")
        ret = ret.filter(
            created__gt=newer_than,
        )

    if args.order_by:
        order_by = [i.strip() for i in args.order_by if i.strip()]
        log.critical(f"FOUND ORDER_BY: {order_by}")
        ret = ret.order_by(*order_by)

    if args.latest_by:
        # ret.order_by("-created", args.latest_by.strip())
        ret = list(ret.values())
        ret.sort(
            key=operator.itemgetter("created"),
            reverse=True,
        )
        ret.sort(
            key=operator.itemgetter(*args.latest_by)
        )
        groups = groupby(
            ret,
            # lambda x: x[args.latest_by]
            key=operator.itemgetter(*args.latest_by)
        )
        return [next(item) for key, item in groups]
    elif args.latest:
        instance = ret.order_by("-created").values().first()
        if instance:
            return [
                # serializer(instance).data
                instance,
            ]
        else:
            return []
    if args.limit is None:
        pass
    else:
        ret = ret[args.offset:args.limit]
    return ret

parser = argparse.ArgumentParser(
    prog="search",
    description="Query the database for events.",
)
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument(
    "--last-15-minutes",
    action="store_true",
)
group.add_argument(
    "--last-hour",
    action="store_true",
)
group.add_argument(
    "--last-day",
    action="store_true",
)
group.add_argument(
    "--last-week",
    action="store_true",
)
group.add_argument(
    "--last-month",
    action="store_true",
)
parser.add_argument(
    "--older-than",
    help="Return events older than the given date. Must be in the format YYYY-MM-DDTHH:MM:SS",
)
parser.add_argument(
    "--newer-than",
    help="Return events newer than the given date. Must be in the format YYYY-MM-DDTHH:MM:SS",
)
parser.add_argument(
    "--order-by",
    action="append",
    help="If provided, it should be the name of a field. "
            "Events will be ordered by that field. Can be "
            "specified multiple times and the ordering will "
            "be applied in order.",
)
parser.add_argument(
    "--limit",
    type=int,
    help="The limit for the number of results to return"
)
parser.add_argument(
    "--offset",
    default=0,
    type=int,
    help="The offset to start from in results to return"
)
parser.add_argument(
    "--latest-by",
    nargs="*",
    help="Return latest result by the given field",
)
parser.add_argument(
    "--latest",
    action="store_true",
    help="If specified, return just the latest event",
)
parser.add_argument(
    "--model",
    default="events.models.Event",
    help="The import_string formatted model to query."
)
# parser.add_argument(
#     "--serializer",
#     default="events.serializers.EventSerializer",
#     help="The serializer to use for results."
# # )
# parser.add_argument(
#     "--database",
#     default="default",
#     help="The database (configured in flashlight settings) to query."
# )
# parser.add_argument(
#     "--user-field",
#     default="user",
#     help="The field on the model that needs to point to logged-in user.",
# )
parser.add_argument(
    "terms",
    nargs="*",
    help="Provide one or more search terms, "
            "must be in the form KEY=VALUE where key "
            "is a reference to a field and VALUE is the value. "
            "For KEY, django field lookups are supported.",
)

@search_command(
    parser,
    input_validators=[
        MustBeFirst,
    ]
)
def search(request, events, argv, environment):
    log = logging.getLogger(__name__)
    # log.info(f"Received {len(events)} events")
    events = resolve(events)
    log.info(f"Received argv: {argv}")

    if "search" in argv:
        argv.pop(argv.index("search"))
    args = search.parser.parse_args(argv)
    if args.latest and args.latest_by:
        raise ValueError("Cannot specify both --latest and --latest-by")

    log.info(f"Parsed args: {args}")

    if events:
        return dict_search(request, events, args)
    else:
        return orm_search(request, events, args)
