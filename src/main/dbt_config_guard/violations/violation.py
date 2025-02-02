from __future__ import annotations

import abc
from abc import ABC
from typing import Generic
from typing import TypeVar

from dbt_config_guard.entities.entity import Entity

E = TypeVar("E", bound=Entity)

class Violation(Generic[E], ABC):
    def __init__(
        self,
        *,
        description: str,
        entity: E,
    ) -> None:
        self._description = description
        self._entity = entity

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        return self._description

    @property
    def entity(self) -> E:
        return self._entity

    def to_dict(self) -> dict:
        return {
            "config_file_path": str(self.entity.config_file_path),
            "entity_type": "model_column",
            "entity_id": self.entity.id,
            "description": self.description,
        }
