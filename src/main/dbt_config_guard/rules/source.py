from __future__ import annotations

from abc import ABC

from dbt_config_guard.entities.source import Source
from dbt_config_guard.rules.rule import Rule

class SourceRule(Rule[Source], ABC):
    pass
