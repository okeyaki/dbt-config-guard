from __future__ import annotations

import abc
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from ruamel.yaml import CommentedMap

class Entity(ABC):
    def __init__(
        self,
        *,
        config: CommentedMap,
    ) -> None:
        self._config = config

    def __eq__(self, rhs: object) -> bool:
        return isinstance(rhs, Entity) and self.id == rhs.id

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    @abc.abstractmethod
    def config_file_path(self) -> Path:
        raise NotImplementedError

    @property
    def config(self) -> CommentedMap:
        return self._config

    @property
    @abc.abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self._config.get("name", "")

    @property
    def description(self) -> str:
        return self.config.get("description", "")
