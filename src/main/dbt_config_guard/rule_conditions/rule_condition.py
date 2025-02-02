from __future__ import annotations

import abc
from abc import ABC
from typing import Generic
from typing import TypeVar

from dbt_config_guard.entities.entity import Entity

E = TypeVar("E", bound=Entity)

class RuleCondition(Generic[E], ABC):
    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: dict | None) -> RuleCondition[E] | None:
        raise NotImplementedError

    @abc.abstractmethod
    def is_satisfied_by(self, entity: E) -> bool:
        raise NotImplementedError
