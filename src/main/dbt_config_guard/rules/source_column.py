from __future__ import annotations

from abc import ABC

from dbt_config_guard.entities.source_column import SourceColumn
from dbt_config_guard.rules.rule import Rule

class SourceColumnRule(Rule[SourceColumn], ABC):
    pass
