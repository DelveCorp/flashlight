import logging
import argparse
from typing import Any, Dict, List

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions, generate_keyword_args

alias_parser = argparse.ArgumentParser(
    prog="alias",
    description="Create aliases for expressions in the QuerySet",
) 
alias_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The field/expression to alias in the QuerySet",
)

@search_command(alias_parser)
def alias(request: HttpRequest, events: QuerySet, argv: List[str], environment: Dict[str, Any]) -> QuerySet:
    """
    Create aliases for expressions in the QuerySet. Aliases are temporary names for expressions that can be used in
    subsequent commands, but aliases will not necessarily be reflected in the output.

    Example:
    ```
    search index=test | qs_alias foo_alias=KT(extracted_fields__foo) bar_alias=KT(extracted_fields__bar) | qs_annotate foo_alias=Sum(foo_alias) bar_alias=Sum(bar_alias)
    ```

    Args:
        request (HttpRequest): The HTTP request object.
        events (QuerySet): The QuerySet to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet with the specified aliases.
    """
    log = logging.getLogger(__name__)
    log.info("In alias")
    args = alias_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"alias can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    positional_args, keyword_args = generate_keyword_args(parsed_expressions)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.alias(*positional_args, **keyword_args)
