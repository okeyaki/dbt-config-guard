from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.rule_conditions.model_column import ModelColumnRuleCondition
from dbt_config_guard.rules.model_column import ModelColumnRule
from dbt_config_guard.rules.rule import RuleSchema
from dbt_config_guard.violations.model_column import ModelColumnViolation

if TYPE_CHECKING:
    from collections.abc import Generator

    from dbt_config_guard.entities.model_column import ModelColumn
    from dbt_config_guard.services.registry import Registry

class ModelColumnDataTestsRequired(ModelColumnRule):
    @classmethod
    def from_config(cls, config: dict) -> ModelColumnDataTestsRequired:
        return cls(
            condition=ModelColumnRuleCondition.from_config(config.get("when")),
            data_test_names=config.get("data_test_names", []),
        )

    @classmethod
    def schema(cls) -> RuleSchema:
        return RuleSchema(
            name="model_columns.data_tests.required",
            description="""
                Model columns should have the specified data tests.
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
        condition: ModelColumnRuleCondition | None,
        data_test_names: list[str],
    ) -> None:
        super().__init__(
            condition=condition,
        )

        self._data_test_names = data_test_names

    def _check(
        self,
        model_column: ModelColumn,
        _registry: Registry,
    ) -> Generator[ModelColumnViolation, None, None]:
        if len(self._data_test_names) == 0:
            return

        for data_test_name in self._data_test_names:
            if not model_column.has_data_test(data_test_name):
                yield ModelColumnViolation(
                    description=f"the model column does not have the specified data test: {data_test_name}",
                    entity=model_column,
                )
