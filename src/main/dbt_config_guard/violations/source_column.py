from __future__ import annotations

from dbt_config_guard.entities.source_column import SourceColumn
from dbt_config_guard.violations.violation import Violation

class SourceColumnViolation(Violation[SourceColumn]):
    def __str__(self) -> str:
        return "\t".join([
            str(self.entity.config_file_path),
            self.entity.id,
            self.description,
        ])
