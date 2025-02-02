from __future__ import annotations

import abc
from abc import ABC
from typing import Generic
from typing import TYPE_CHECKING
from typing import TypeVar

from dbt_config_guard.entities.entity import Entity
from dbt_config_guard.utils.text import TextUtils

if TYPE_CHECKING:
    from collections.abc import Generator

    from dbt_config_guard.rule_conditions.rule_condition import RuleCondition
    from dbt_config_guard.services.registry import Registry
    from dbt_config_guard.violations.violation import Violation

class RuleSchema:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        custom_options: dict | None = None,
    ) -> None:
        if custom_options is None:
            custom_options = {}

        self._name = name
        self._description = description
        self._custom_options = custom_options

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def options(self) -> dict:
        return {
            **self.common_options,
            **self.custom_options,
        }

    @property
    def common_options(self) -> dict:
        return {}

    @property
    def custom_options(self) -> dict:
        return self._custom_options

    def to_json_schema(self) -> dict:
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": self.name,
            "description": TextUtils.dedent(self.description),
            "type": "object",
            "additionalProperties": False,
            "properties": {
                **self.options,
            },
        }

E = TypeVar("E", bound=Entity)

class Rule(Generic[E], ABC):
    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: dict) -> Rule[E]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def schema(cls) -> RuleSchema:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def default_config(cls) -> bool | dict:
        raise NotImplementedError

    def __init__(
        self,
        condition: RuleCondition[E] | None,
    ) -> None:
        self._condition = condition

    @property
    def condition(self) -> RuleCondition[E] | None:
        return self._condition

    def check(self, entity: E, registry: Registry) -> Generator[Violation[E], None, None]:
        if self.condition and not self.condition.is_satisfied_by(entity):
            return

        yield from self._check(entity, registry)

    @abc.abstractmethod
    def _check(self, entity: E, registry: Registry) -> Generator[Violation[E], None, None]:
        raise NotImplementedError
