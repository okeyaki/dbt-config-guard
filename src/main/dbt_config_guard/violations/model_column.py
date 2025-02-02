from __future__ import annotations

from dbt_config_guard.entities.model_column import ModelColumn
from dbt_config_guard.violations.violation import Violation

class ModelColumnViolation(Violation[ModelColumn]):
    def __str__(self) -> str:
        return "\t".join([
            str(self.entity.config_file_path),
            self.entity.id,
            self.description,
        ])
