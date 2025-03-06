import logging
import argparse
from typing import Any, Dict, List

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions, generate_keyword_args

having_parser = argparse.ArgumentParser(
    prog="having",
    description="Filter grouped records from the QuerySet based on the provided expressions",
) 
having_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The field/expression to filter grouped records from the QuerySet",
)

@search_command(having_parser)
def having(request: HttpRequest, events: QuerySet, argv: List[str], environment: Dict[str, Any]) -> QuerySet:
    """
    Filter grouped records from the QuerySet based on the provided expressions.

    Args:
        request (HttpRequest): The HTTP request object.
        events (QuerySet): The QuerySet to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet with filtered grouped records.
    """
    log = logging.getLogger(__name__)
    log.info("In having")
    args = having_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"having can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    positional_args, keyword_args = generate_keyword_args(parsed_expressions)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.filter(*positional_args, **keyword_args)
