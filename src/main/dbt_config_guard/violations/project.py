from __future__ import annotations

from dbt_config_guard.entities.project import Project
from dbt_config_guard.violations.violation import Violation

class ProjectViolation(Violation[Project]):
    def __str__(self) -> str:
        return f"{self.entity.id}: {self.description}"
