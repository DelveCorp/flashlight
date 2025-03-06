import logging
import argparse
from typing import Any, Dict, List

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.search_commands.decorators import search_command

earliest_parser = argparse.ArgumentParser(
    prog="earliest",
    description="Return the earliest record in the QuerySet based on the provided field",
)

earliest_parser.add_argument(
    "field",
    help="The field to determine the earliest record",
)

@search_command(earliest_parser)
def earliest(request: HttpRequest, events: QuerySet, argv: List[str], environment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return the earliest record in the QuerySet based on the provided field.

    Args:
        request (HttpRequest): The HTTP request object.
        events (QuerySet): The QuerySet to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        Dict[str, Any]: The earliest record in the QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In earliest")
    args = earliest_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"earliest can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.earliest(args.field)
