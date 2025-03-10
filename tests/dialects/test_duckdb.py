from tests.dialects.test_dialect import Validator


class TestDuckDB(Validator):
    dialect = "duckdb"

    def test_time(self):
        self.validate_all(
            "EPOCH(x)",
            read={
                "presto": "TO_UNIXTIME(x)",
            },
            write={
                "bigquery": "TIME_TO_UNIX(x)",
                "duckdb": "EPOCH(x)",
                "presto": "TO_UNIXTIME(x)",
                "spark": "UNIX_TIMESTAMP(x)",
            },
        )
        self.validate_all(
            "EPOCH_MS(x)",
            write={
                "bigquery": "UNIX_TO_TIME(x / 1000)",
                "duckdb": "TO_TIMESTAMP(CAST(x / 1000 AS BIGINT))",
                "presto": "FROM_UNIXTIME(x / 1000)",
                "spark": "FROM_UNIXTIME(x / 1000)",
            },
        )
        self.validate_all(
            "STRFTIME(x, '%y-%-m-%S')",
            write={
                "bigquery": "TIME_TO_STR(x, '%y-%-m-%S')",
                "duckdb": "STRFTIME(x, '%y-%-m-%S')",
                "postgres": "TO_CHAR(x, 'YY-FMMM-SS')",
                "presto": "DATE_FORMAT(x, '%y-%c-%S')",
                "spark": "DATE_FORMAT(x, 'yy-M-ss')",
            },
        )
        self.validate_all(
            "STRFTIME(x, '%Y-%m-%d %H:%M:%S')",
            write={
                "duckdb": "STRFTIME(x, '%Y-%m-%d %H:%M:%S')",
                "presto": "DATE_FORMAT(x, '%Y-%m-%d %H:%i:%S')",
                "hive": "DATE_FORMAT(x, 'yyyy-MM-dd HH:mm:ss')",
            },
        )
        self.validate_all(
            "STRPTIME(x, '%y-%-m')",
            write={
                "bigquery": "STR_TO_TIME(x, '%y-%-m')",
                "duckdb": "STRPTIME(x, '%y-%-m')",
                "presto": "DATE_PARSE(x, '%y-%c')",
                "hive": "CAST(FROM_UNIXTIME(UNIX_TIMESTAMP(x, 'yy-M')) AS TIMESTAMP)",
                "spark": "TO_TIMESTAMP(x, 'yy-M')",
            },
        )
        self.validate_all(
            "TO_TIMESTAMP(x)",
            write={
                "duckdb": "CAST(x AS TIMESTAMP)",
                "presto": "DATE_PARSE(x, '%Y-%m-%d %H:%i:%s')",
                "hive": "CAST(x AS TIMESTAMP)",
            },
        )

    def test_duckdb(self):
        self.validate_all(
            "LIST_VALUE(0, 1, 2)",
            write={
                "bigquery": "[0, 1, 2]",
                "duckdb": "LIST_VALUE(0, 1, 2)",
                "presto": "ARRAY[0, 1, 2]",
                "spark": "ARRAY(0, 1, 2)",
            },
        )
        self.validate_all(
            "REGEXP_MATCHES(x, y)",
            write={
                "duckdb": "REGEXP_MATCHES(x, y)",
                "presto": "REGEXP_LIKE(x, y)",
                "hive": "x RLIKE y",
                "spark": "x RLIKE y",
            },
        )
        self.validate_all(
            "STR_SPLIT(x, 'a')",
            write={
                "duckdb": "STR_SPLIT(x, 'a')",
                "presto": "SPLIT(x, 'a')",
                "hive": "SPLIT(x, CONCAT('\\\\Q', 'a'))",
                "spark": "SPLIT(x, CONCAT('\\\\Q', 'a'))",
            },
        )
        self.validate_all(
            "STRING_TO_ARRAY(x, 'a')",
            write={
                "duckdb": "STR_SPLIT(x, 'a')",
                "presto": "SPLIT(x, 'a')",
                "hive": "SPLIT(x, CONCAT('\\\\Q', 'a'))",
                "spark": "SPLIT(x, CONCAT('\\\\Q', 'a'))",
            },
        )
        self.validate_all(
            "STR_SPLIT_REGEX(x, 'a')",
            write={
                "duckdb": "STR_SPLIT_REGEX(x, 'a')",
                "presto": "REGEXP_SPLIT(x, 'a')",
                "hive": "SPLIT(x, 'a')",
                "spark": "SPLIT(x, 'a')",
            },
        )
        self.validate_all(
            "STRUCT_EXTRACT(x, 'abc')",
            write={
                "duckdb": "STRUCT_EXTRACT(x, 'abc')",
                "presto": 'x."abc"',
                "hive": "x.`abc`",
                "spark": "x.`abc`",
            },
        )
        self.validate_all(
            "STRUCT_EXTRACT(STRUCT_EXTRACT(x, 'y'), 'abc')",
            write={
                "duckdb": "STRUCT_EXTRACT(STRUCT_EXTRACT(x, 'y'), 'abc')",
                "presto": 'x."y"."abc"',
                "hive": "x.`y`.`abc`",
                "spark": "x.`y`.`abc`",
            },
        )

        self.validate_all(
            "QUANTILE(x, 0.5)",
            write={
                "duckdb": "QUANTILE(x, 0.5)",
                "presto": "APPROX_PERCENTILE(x, 0.5)",
                "hive": "PERCENTILE(x, 0.5)",
                "spark": "PERCENTILE(x, 0.5)",
            },
        )

        self.validate_all(
            "CAST(x AS DATE)",
            write={
                "duckdb": "CAST(x AS DATE)",
                "": "CAST(x AS DATE)",
            },
        )
        self.validate_all(
            "UNNEST(x)",
            read={
                "spark": "EXPLODE(x)",
            },
            write={
                "duckdb": "UNNEST(x)",
                "spark": "EXPLODE(x)",
            },
        )

        self.validate_all(
            "1d",
            write={
                "duckdb": "1 AS d",
                "spark": "1 AS d",
            },
        )
        self.validate_all(
            "CAST(1 AS DOUBLE)",
            read={
                "hive": "1d",
                "spark": "1d",
            },
        )
        self.validate_all(
            "POWER(CAST(2 AS SMALLINT), 3)",
            read={
                "hive": "POW(2S, 3)",
                "spark": "POW(2S, 3)",
            },
        )
        self.validate_all(
            "LIST_SUM(LIST_VALUE(1, 2))",
            read={
                "spark": "ARRAY_SUM(ARRAY(1, 2))",
            },
        )
        self.validate_all(
            "IF(y <> 0, x / y, NULL)",
            read={
                "bigquery": "SAFE_DIVIDE(x, y)",
            },
        )
        self.validate_all(
            "STRUCT_PACK(x := 1, y := '2')",
            write={
                "duckdb": "STRUCT_PACK(x := 1, y := '2')",
                "spark": "STRUCT(x = 1, y = '2')",
            },
        )
        self.validate_all(
            "ARRAY_SORT(x)",
            write={
                "duckdb": "ARRAY_SORT(x)",
                "presto": "ARRAY_SORT(x)",
                "hive": "SORT_ARRAY(x)",
                "spark": "SORT_ARRAY(x)",
            },
        )
        self.validate_all(
            "ARRAY_REVERSE_SORT(x)",
            write={
                "duckdb": "ARRAY_REVERSE_SORT(x)",
                "presto": "ARRAY_SORT(x, (a, b) -> CASE WHEN a < b THEN 1 WHEN a > b THEN -1 ELSE 0 END)",
                "hive": "SORT_ARRAY(x, FALSE)",
                "spark": "SORT_ARRAY(x, FALSE)",
            },
        )
        self.validate_all(
            "LIST_REVERSE_SORT(x)",
            write={
                "duckdb": "ARRAY_REVERSE_SORT(x)",
                "presto": "ARRAY_SORT(x, (a, b) -> CASE WHEN a < b THEN 1 WHEN a > b THEN -1 ELSE 0 END)",
                "hive": "SORT_ARRAY(x, FALSE)",
                "spark": "SORT_ARRAY(x, FALSE)",
            },
        )
        self.validate_all(
            "LIST_SORT(x)",
            write={
                "duckdb": "ARRAY_SORT(x)",
                "presto": "ARRAY_SORT(x)",
                "hive": "SORT_ARRAY(x)",
                "spark": "SORT_ARRAY(x)",
            },
        )
        self.validate_all(
            "SELECT fname, lname, age FROM person ORDER BY age DESC NULLS FIRST, fname ASC NULLS LAST, lname",
            write={
                "duckdb": "SELECT fname, lname, age FROM person ORDER BY age DESC NULLS FIRST, fname NULLS LAST, lname",
            },
        )
        self.validate_all(
            "MONTH('2021-03-01')",
            write={
                "duckdb": "MONTH('2021-03-01')",
                "presto": "MONTH('2021-03-01')",
                "hive": "MONTH('2021-03-01')",
                "spark": "MONTH('2021-03-01')",
            },
        )
