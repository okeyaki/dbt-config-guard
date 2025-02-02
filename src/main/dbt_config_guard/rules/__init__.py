from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path

from dbt_config_guard.rules.rule import Rule

def _import_rule_classes() -> dict[str, type[Rule]]:
    rule_classes: dict[str, type[Rule]] = {}
    for module_info in pkgutil.iter_modules([
        Path(__file__).parent.resolve().as_posix(),
    ]):
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if not inspect.isclass(attribute):
                continue

            if not issubclass(attribute, Rule):
                continue

            if inspect.isabstract(attribute):
                continue

            rule_classes[attribute_name] = attribute

    return rule_classes

RULE_CLASSES = _import_rule_classes()
