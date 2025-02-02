from __future__ import annotations

from abc import ABC

from dbt_config_guard.entities.model import Model
from dbt_config_guard.rules.rule import Rule

class ModelRule(Rule[Model], ABC):
    pass
