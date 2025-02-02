from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.rule_conditions.source_column import SourceColumnRuleCondition
from dbt_config_guard.rules.rule import RuleSchema
from dbt_config_guard.rules.source_column import SourceColumnRule
from dbt_config_guard.violations.source_column import SourceColumnViolation

if TYPE_CHECKING:
    from collections.abc import Generator

    from dbt_config_guard.entities.source_column import SourceColumn
    from dbt_config_guard.services.registry import Registry

class SourceColumnDataTestsRequired(SourceColumnRule):
    @classmethod
    def from_config(cls, config: dict) -> SourceColumnDataTestsRequired:
        return cls(
            condition=SourceColumnRuleCondition.from_config(config.get("when")),
            data_test_names=config.get("data_test_names", []),
        )

    @classmethod
    def schema(cls) -> RuleSchema:
        return RuleSchema(
            name="source_columns.data_tests.required",
            description="""
                Source columns should have the specified data tests.
            """,
            custom_options={
                "data_test_names": {
                    "description": "Required data test names.",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "examples": [
                            "not_null",
                        ],
                    },
                },
            },
        )

    @classmethod
    def default_config(cls) -> bool | dict:
        return True

    def __init__(
        self,
        *,
        condition: SourceColumnRuleCondition | None,
        data_test_names: list[str],
    ) -> None:
        super().__init__(
            condition=condition,
        )

        self._data_test_names = data_test_names

    def _check(
        self,
        source_column: SourceColumn,
        _registry: Registry,
    ) -> Generator[SourceColumnViolation, None, None]:
        if len(self._data_test_names) == 0:
            return

        for data_test_name in self._data_test_names:
            if not source_column.has_data_test(data_test_name):
                yield SourceColumnViolation(
                    description=f"the source column does not have the specified data test: {data_test_name}",
                    entity=source_column,
                )
