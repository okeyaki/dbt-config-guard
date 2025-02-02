import json

from dbt_config_guard.formatters.formatter import Formatter
from dbt_config_guard.violations.violation import Violation

class JsonFormatter(Formatter):
    def format(self, violation: Violation) -> str:
        return json.dumps(
            violation.to_dict(),
            ensure_ascii=False,
        )
