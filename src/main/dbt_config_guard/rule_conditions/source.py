from __future__ import annotations

import re

from dbt_config_guard.entities.source import Source
from dbt_config_guard.rule_conditions.rule_condition import RuleCondition

class SourceRuleCondition(RuleCondition[Source]):
    @classmethod
    def from_config(cls, config: dict | None) -> SourceRuleCondition | None:
        if config is None:
            return None

        return SourceRuleCondition(
            source_names=config.get("source_names", []),
        )

    def __init__(
        self,
        source_names: list[str],
    ) -> None:
        self.source_names = source_names

    def is_satisfied_by(self, source: Source) -> bool:
        is_satisfied = True

        for source_name in self.source_names:
            if not re.match(source_name, source.name):
                is_satisfied = False

        return is_satisfied
