import unittest

from sqlglot.expressions import Func
from sqlglot.parser import Parser
from sqlglot.tokens import Tokenizer


class TestGenerator(unittest.TestCase):
    def test_fallback_function_sql(self):
        class SpecialUDF(Func):
            arg_types = {"a": True, "b": False}

        class NewParser(Parser):
            FUNCTIONS = SpecialUDF.default_parser_mappings()

        tokens = Tokenizer().tokenize("SELECT SPECIAL_UDF(a) FROM x")
        expression = NewParser().parse(tokens)[0]
        self.assertEqual(expression.sql(), "SELECT SPECIAL_UDF(a) FROM x")

    def test_fallback_function_var_args_sql(self):
        class SpecialUDF(Func):
            arg_types = {"a": True, "expressions": False}
            is_var_len_args = True

        class NewParser(Parser):
            FUNCTIONS = SpecialUDF.default_parser_mappings()

        tokens = Tokenizer().tokenize("SELECT SPECIAL_UDF(a, b, c, d + 1) FROM x")
        expression = NewParser().parse(tokens)[0]
        self.assertEqual(expression.sql(), "SELECT SPECIAL_UDF(a, b, c, d + 1) FROM x")
