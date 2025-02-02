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

class SourceColumnDescriptionRequired(SourceColumnRule):
    @classmethod
    def from_config(cls, config: dict) -> SourceColumnDescriptionRequired:
        return cls(
            condition=SourceColumnRuleCondition.from_config(config.get("when")),
        )

    @classmethod
    def schema(cls) -> RuleSchema:
        return RuleSchema(
            name="source_columns.description.required",
            description="""
                Source columns should have the description.
            """,
        )

    @classmethod
    def default_config(cls) -> bool | dict:
        return True

    def _check(
        self,
        source_column: SourceColumn,
        _registry: Registry,
    ) -> Generator[SourceColumnViolation, None, None]:
        if source_column.description == "":
            yield SourceColumnViolation(
                description="the source column does not have the description",
                entity=source_column,
           )
