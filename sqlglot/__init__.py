from sqlglot import expressions as exp
from sqlglot.dialects import Dialect, Dialects
from sqlglot.diff import diff
from sqlglot.errors import ErrorLevel, UnsupportedError, ParseError, TokenError
from sqlglot.expressions import (
    Expression,
    select,
    from_,
    and_,
    or_,
    not_,
    condition,
    alias_ as alias,
    column,
    table_ as table,
    subquery,
)
from sqlglot.generator import Generator
from sqlglot.tokens import Tokenizer, TokenType
from sqlglot.parser import Parser


__version__ = "5.3.1"

pretty = False


def parse(sql, read=None, **opts):
    """
    Parses the given SQL string into a collection of syntax trees, one per
    parsed SQL statement.

    Args:
        sql (str): the SQL code string to parse.
        read (str): the SQL dialect to apply during parsing
            (eg. "spark", "hive", "presto", "mysql").
        **opts: other options.

    Returns:
        typing.List[Expression]: the list of parsed syntax trees.
    """
    dialect = Dialect.get_or_raise(read)()
    return dialect.parse(sql, **opts)


def parse_one(sql, read=None, into=None, **opts):
    """
    Parses the given SQL string and returns a syntax tree for the first
    parsed SQL statement.

    Args:
        sql (str): the SQL code string to parse.
        read (str): the SQL dialect to apply during parsing
            (eg. "spark", "hive", "presto", "mysql").
        into (Expression): the SQLGlot Expression to parse into
        **opts: other options.

    Returns:
        Expression: the syntax tree for the first parsed statement.
    """

    dialect = Dialect.get_or_raise(read)()

    if into:
        result = dialect.parse_into(into, sql, **opts)
    else:
        result = dialect.parse(sql, **opts)

    return result[0] if result else None


def transpile(sql, read=None, write=None, identity=True, error_level=None, **opts):
    """
    Parses the given SQL string using the source dialect and returns a list of SQL strings
    transformed to conform to the target dialect. Each string in the returned list represents
    a single transformed SQL statement.

    Args:
        sql (str): the SQL code string to transpile.
        read (str): the source dialect used to parse the input string
            (eg. "spark", "hive", "presto", "mysql").
        write (str): the target dialect into which the input should be transformed
            (eg. "spark", "hive", "presto", "mysql").
        identity (bool): if set to True and if the target dialect is not specified
            the source dialect will be used as both: the source and the target dialect.
        error_level (ErrorLevel): the desired error level of the parser.
        **opts: other options.

    Returns:
        typing.List[str]: the list of transpiled SQL statements / expressions.
    """
    write = write or read if identity else write
    return [
        Dialect.get_or_raise(write)().generate(expression, **opts)
        for expression in parse(sql, read, error_level=error_level)
    ]
