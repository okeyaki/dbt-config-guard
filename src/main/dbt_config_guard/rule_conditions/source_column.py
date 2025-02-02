from __future__ import annotations

import re

from dbt_config_guard.entities.source_column import SourceColumn
from dbt_config_guard.rule_conditions.rule_condition import RuleCondition

class SourceColumnRuleCondition(RuleCondition[SourceColumn]):
    @classmethod
    def from_config(cls, config: dict | None) -> SourceColumnRuleCondition | None:
        if config is None:
            return None

        return SourceColumnRuleCondition(
            source_names=config.get("source_names", []),
            source_column_names=config.get("source_column_names", []),
            source_column_data_types=config.get("source_column_data_types", []),
        )

    def __init__(
        self,
        source_names: list[str],
        source_column_names: list[str],
        source_column_data_types: list[str],
    ) -> None:
        self.source_names = source_names
        self.source_column_names = source_column_names
        self.source_column_data_types = source_column_data_types

    def is_satisfied_by(self, source_column: SourceColumn) -> bool:
        is_satisfied = True

        for source_name in self.source_names:
            if not re.match(source_name, source_column.source.name):
                is_satisfied = False

        for source_column_name in self.source_column_names:
            if not re.match(source_column_name, source_column.name):
                is_satisfied = False

        for source_column_data_type in self.source_column_data_types:
            if not re.match(source_column_data_type, source_column.data_type):
                is_satisfied = False

        return is_satisfied
