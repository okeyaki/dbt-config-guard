from __future__ import annotations

from abc import ABC

from dbt_config_guard.entities.model_column import ModelColumn
from dbt_config_guard.rules.rule import Rule

class ModelColumnRule(Rule[ModelColumn], ABC):
    pass
