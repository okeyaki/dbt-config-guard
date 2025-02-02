from dbt_config_guard.formatters.formatter import Formatter
from dbt_config_guard.violations.violation import Violation

class LtsvFormatter(Formatter):
    def format(self, violation: Violation) -> str:
        return "\t".join([
            f"{k}:{v}"
            for k, v
            in violation.to_dict().items()
        ])
