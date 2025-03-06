import logging
import argparse
from typing import Any, Dict, List

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.search_commands.decorators import search_command
from events.search_commands.util import has_permission_for_model

delete_parser = argparse.ArgumentParser(
    prog="delete",
    description="Delete records from the QuerySet",
)

@search_command(delete_parser)
def delete(request: HttpRequest, events: QuerySet, argv: List[str], environment: Dict[str, Any]) -> int:
    """
    Delete records from the QuerySet.

    Args:
        request (HttpRequest): The HTTP request object.
        events (QuerySet): The QuerySet to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        int: The number of records deleted.
    """
    log = logging.getLogger(__name__)
    log.info("In delete")
    args = delete_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"delete can only operate on QuerySets like "
            "the output of the search command"
        )

    model = events.query.model
    if not has_permission_for_model('delete', model, request):
        raise PermissionError("Permission denied")


    log.debug(f"Received {args=}")
    deleted_count, _ = events.delete()
    return deleted_count
