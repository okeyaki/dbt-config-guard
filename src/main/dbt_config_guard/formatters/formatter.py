import abc
from abc import ABC

from dbt_config_guard.violations.violation import Violation

class Formatter(ABC):
    @abc.abstractmethod
    def format(self, violation: Violation) -> str:
        raise NotImplementedError
