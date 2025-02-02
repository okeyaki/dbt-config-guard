from dbt_config_guard.formatters.formatter import Formatter
from dbt_config_guard.violations.violation import Violation

class TextFormatter(Formatter):
    def format(self, violation: Violation) -> str:
        return str(violation)
