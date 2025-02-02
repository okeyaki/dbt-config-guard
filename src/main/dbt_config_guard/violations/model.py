from __future__ import annotations

from dbt_config_guard.entities.model import Model
from dbt_config_guard.violations.violation import Violation

class ModelViolation(Violation[Model]):
    def __str__(self) -> str:
        return "\t".join([
            str(self.entity.config_file_path),
            self.entity.id,
            self.description,
        ])
