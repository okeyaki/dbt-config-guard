from __future__ import annotations

from abc import ABC
from typing import Generic
from typing import TYPE_CHECKING
from typing import TypeVar

from ruamel.yaml import CommentedMap
from ruamel.yaml import CommentedSeq

from dbt_config_guard.entities.entity import Entity
from dbt_config_guard.rules import RULE_CLASSES

if TYPE_CHECKING:
    from collections.abc import Generator

    from dbt_config_guard.rules.rule import Rule
    from dbt_config_guard.services.registry import Registry
    from dbt_config_guard.violations.violation import Violation

E = TypeVar("E", bound=Entity)

class Ruleset(Generic[E], ABC):
    CONFIG_KEY_PREFIX = "rules."

    @classmethod
    def from_config(
        cls,
        rule_classes: list[type[Rule[E]]],
        config: dict,
    ) -> Ruleset[E]:
        rules: list[Rule[E]] = []
        for rule_class in rule_classes:
            config_key = f"{cls.CONFIG_KEY_PREFIX}{rule_class.schema().name}"

            if config_key not in config:
                continue

            config_value = config[config_key]

            # <config_key>: true
            if type(config_value) is bool:
                if config_value:
                    rules.append(rule_class.from_config({}))

                continue

            # <config_key>:
            #    <config_value>
            if type(config_value) is CommentedMap:
                rules.append(rule_class.from_config(config_value))

                continue

            # <config_key>:
            #    - <config_value>
            #    - <config_value>
            if type(config_value) is CommentedSeq:
                rules.extend([rule_class.from_config(e) for e in config_value])

                continue

        return cls(rules)

    @classmethod
    def default_config(cls) -> CommentedMap:
        return CommentedMap({
            f"{cls.CONFIG_KEY_PREFIX}{e.schema().name}": e.default_config()
            for e
            in RULE_CLASSES.values()
        })

    def __init__(self, rules: list[Rule[E]]) -> None:
        self._rules = rules

    def check(self, entity: E, registry: Registry) -> Generator[Violation[E], None, None]:
        for rule in self._rules:
            yield from rule.check(entity, registry)
