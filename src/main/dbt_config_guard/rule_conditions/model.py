from __future__ import annotations

import re

from dbt_config_guard.entities.model import Model
from dbt_config_guard.rule_conditions.rule_condition import RuleCondition

class ModelRuleCondition(RuleCondition[Model]):
    @classmethod
    def from_config(cls, config: dict | None) -> ModelRuleCondition | None:
        if config is None:
            return None

        return ModelRuleCondition(
            model_names=config.get("model_names", []),
        )

    def __init__(
        self,
        model_names: list[str],
    ) -> None:
        self.model_names = model_names

    def is_satisfied_by(self, model: Model) -> bool:
        is_satisfied = True

        for model_name in self.model_names:
            if not re.match(model_name, model.name):
                is_satisfied = False

        return is_satisfied
