from __future__ import annotations

from unittest.mock import MagicMock

from dbt_config_guard.rules.model_column_description_required import ModelColumnDescriptionRequired

from test.fixtures.model_column import ModelColumnFixture

def test__check__ok(
) -> None:
    model_column_fixture = ModelColumnFixture.with_defaults()
    model_column_fixture.description = "the customer id"
    model_column = model_column_fixture.create()

    registry = MagicMock()

    rule = ModelColumnDescriptionRequired(
        condition=None,
    )

    model_column_violations = list(rule.check(model_column, registry))

    assert len(model_column_violations) == 0

def test__check__ng(
) -> None:
    model_column_fixture = ModelColumnFixture.with_defaults()
    model_column_fixture.description = ""
    model_column = model_column_fixture.create()

    registry = MagicMock()

    rule = ModelColumnDescriptionRequired(
        condition=None,
    )

    model_column_violations = list(rule.check(model_column, registry))

    assert len(model_column_violations) == 1
    assert model_column_violations[0].description == "the model column does not have the description"
    assert model_column_violations[0].entity == model_column
