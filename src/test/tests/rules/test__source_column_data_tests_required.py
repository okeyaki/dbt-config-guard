from __future__ import annotations

from unittest.mock import MagicMock

from dbt_config_guard.rules.source_column_data_tests_required import SourceColumnDataTestsRequired

from test.fixtures.source_column import SourceColumnFixture

def test__check__ok(
) -> None:
    source_column_fixture = SourceColumnFixture.with_defaults()
    source_column_fixture.data_tests = [
        "unique",
        "not_null",
        {
            "dbt_utils.not_empty_string": {
                "trim_whitespace": False,
            },
        },
    ]
    source_column = source_column_fixture.create()

    registry = MagicMock()

    rule = SourceColumnDataTestsRequired(
        condition=None,
        data_test_names=[
            "unique",
            "not_null",
            "dbt_utils.not_empty_string",
        ],
    )
    source_column_violations = list(rule.check(source_column, registry))

    assert len(source_column_violations) == 0

def test__check__ng(
) -> None:
    source_column_fixture = SourceColumnFixture.with_defaults()
    source_column_fixture.data_tests = []
    source_column = source_column_fixture.create()

    registry = MagicMock()

    rule = SourceColumnDataTestsRequired(
        condition=None,
        data_test_names=[
            "unique",
            "not_null",
            "dbt_utils.not_empty_string",
        ],
    )
    source_column_violations = list(rule.check(source_column, registry))

    assert len(source_column_violations) == 3
    assert source_column_violations[0].description == "the source column does not have the specified data test: unique"
    assert source_column_violations[0].entity == source_column
    assert source_column_violations[1].description == "the source column does not have the specified data test: not_null"
    assert source_column_violations[1].entity == source_column
    assert source_column_violations[2].description == "the source column does not have the specified data test: dbt_utils.not_empty_string"
    assert source_column_violations[2].entity == source_column
