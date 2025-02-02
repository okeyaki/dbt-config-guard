from __future__ import annotations

from unittest.mock import MagicMock

from dbt_config_guard.rules.model_column_data_tests_required import ModelColumnDataTestsRequired

from test.fixtures.model_column import ModelColumnFixture

def test__check__ok(
) -> None:
    model_column_fixture = ModelColumnFixture.with_defaults()
    model_column_fixture.data_tests = [
        "unique",
        "not_null",
        {
            "dbt_utils.not_empty_string": {
                "trim_whitespace": False,
            },
        },
    ]
    model_column = model_column_fixture.create()

    registry = MagicMock()

    rule = ModelColumnDataTestsRequired(
        condition=None,
        data_test_names=[
            "unique",
            "not_null",
            "dbt_utils.not_empty_string",
        ],
    )
    model_column_violations = list(rule.check(model_column, registry))

    assert len(model_column_violations) == 0

def test__check__ng(
) -> None:
    model_column_fixture = ModelColumnFixture.with_defaults()
    model_column_fixture.data_tests = []
    model_column = model_column_fixture.create()

    registry = MagicMock()

    rule = ModelColumnDataTestsRequired(
        condition=None,
        data_test_names=[
            "unique",
            "not_null",
            "dbt_utils.not_empty_string",
        ],
    )
    model_column_violations = list(rule.check(model_column, registry))

    assert len(model_column_violations) == 3
    assert model_column_violations[0].description == "the model column does not have the specified data test: unique"
    assert model_column_violations[0].entity == model_column
    assert model_column_violations[1].description == "the model column does not have the specified data test: not_null"
    assert model_column_violations[1].entity == model_column
    assert model_column_violations[2].description == "the model column does not have the specified data test: dbt_utils.not_empty_string"
    assert model_column_violations[2].entity == model_column
