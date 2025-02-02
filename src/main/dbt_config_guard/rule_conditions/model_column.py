from __future__ import annotations

import re

from dbt_config_guard.entities.model_column import ModelColumn
from dbt_config_guard.rule_conditions.rule_condition import RuleCondition

class ModelColumnRuleCondition(RuleCondition[ModelColumn]):
    @classmethod
    def from_config(cls, config: dict | None) -> ModelColumnRuleCondition | None:
        if config is None:
            return None

        return ModelColumnRuleCondition(
            model_names=config.get("model_names", []),
            model_column_names=config.get("model_column_names", []),
            model_column_data_types=config.get("model_column_data_types", []),
        )

    def __init__(
        self,
        model_names: list[str],
        model_column_names: list[str],
        model_column_data_types: list[str],
    ) -> None:
        self.model_names = model_names
        self.model_column_names = model_column_names
        self.model_column_data_types = model_column_data_types

    def is_satisfied_by(self, model_column: ModelColumn) -> bool:
        is_satisfied = True

        for model_name in self.model_names:
            if not re.match(model_name, model_column.model.name):
                is_satisfied = False

        for model_column_name in self.model_column_names:
            if not re.match(model_column_name, model_column.name):
                is_satisfied = False

        for model_column_data_type in self.model_column_data_types:
            if not re.match(model_column_data_type, model_column.data_type):
                is_satisfied = False

        return is_satisfied
