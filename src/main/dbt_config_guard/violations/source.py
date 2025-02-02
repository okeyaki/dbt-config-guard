from __future__ import annotations

from dbt_config_guard.entities.source import Source
from dbt_config_guard.violations.violation import Violation

class SourceViolation(Violation[Source]):
    def __str__(self) -> str:
        return "\t".join([
            str(self.entity.config_file_path),
            self.entity.id,
            self.description,
        ])
