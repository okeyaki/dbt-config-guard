from __future__ import annotations

from abc import ABC

from dbt_config_guard.entities.project import Project
from dbt_config_guard.rules.rule import Rule

class ProjectRule(Rule[Project], ABC):
    pass
