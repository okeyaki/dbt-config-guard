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

class ModelColumnDescriptionConsistent(ModelColumnRule):
    @classmethod
    def from_config(cls, config: dict) -> ModelColumnDescriptionConsistent:
        return cls(
            condition=ModelColumnRuleCondition.from_config(config.get("when")),
        )

    @classmethod
    def schema(cls) -> RuleSchema:
        return RuleSchema(
            name="model_columns.description.consistent",
            description="""
                Model columns with the same name should have the same description.
            """,
        )

    @classmethod
    def default_config(cls) -> bool | dict:
        return True

    def _check(
        self,
        model_column: ModelColumn,
        registry: Registry,
    ) -> Generator[ModelColumnViolation, None, None]:
        for another_model_column in registry.find_model_columns_by_name(model_column.name):
            if model_column == another_model_column:
                continue

            yield ModelColumnViolation(
                description="the model columns with the same name has different descriptions",
                entity=model_column,
            )
