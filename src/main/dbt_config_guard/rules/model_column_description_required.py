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

class ModelColumnDescriptionRequired(ModelColumnRule):
    @classmethod
    def from_config(cls, config: dict) -> ModelColumnDescriptionRequired:
        return cls(
            condition=ModelColumnRuleCondition.from_config(config.get("when")),
        )

    @classmethod
    def schema(cls) -> RuleSchema:
        return RuleSchema(
            name="model_columns.description.required",
            description="""
                Model columns should have the description.
            """,
        )

    @classmethod
    def default_config(cls) -> bool | dict:
        return True

    def _check(
        self,
        model_column: ModelColumn,
        _registry: Registry,
    ) -> Generator[ModelColumnViolation, None, None]:
        if model_column.description == "":
            yield ModelColumnViolation(
                description="the model column does not have the description",
                entity=model_column,
           )
