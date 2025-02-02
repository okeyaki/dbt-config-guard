from __future__ import annotations

import abc
from abc import ABC
from typing import Generic
from typing import TypeVar

T = TypeVar("T")

class Fixture(Generic[T], ABC):
    @classmethod
    @abc.abstractmethod
    def with_defaults(cls) -> Fixture[T]:
        raise NotImplementedError

    def create(self) -> T:
        return self._build()

    @abc.abstractmethod
    def _build(self) -> T:
        raise NotImplementedError
