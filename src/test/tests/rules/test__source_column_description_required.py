from __future__ import annotations

from unittest.mock import MagicMock

from dbt_config_guard.rules.source_column_description_required import SourceColumnDescriptionRequired

from test.fixtures.source_column import SourceColumnFixture

def test__check__ok(
) -> None:
    source_column_fixture = SourceColumnFixture.with_defaults()
    source_column_fixture.description = "the customer id"
    source_column = source_column_fixture.create()

    registry = MagicMock()

    rule = SourceColumnDescriptionRequired(
        condition=None,
    )

    source_column_violations = list(rule.check(source_column, registry))

    assert len(source_column_violations) == 0

def test__check__ng(
) -> None:
    source_column_fixture = SourceColumnFixture.with_defaults()
    source_column_fixture.description = ""
    source_column = source_column_fixture.create()

    registry = MagicMock()

    rule = SourceColumnDescriptionRequired(
        condition=None,
    )

    source_column_violations = list(rule.check(source_column, registry))

    assert len(source_column_violations) == 1
    assert source_column_violations[0].description == "the source column does not have the description"
    assert source_column_violations[0].entity == source_column
