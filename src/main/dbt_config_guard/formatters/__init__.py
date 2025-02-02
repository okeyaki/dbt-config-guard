from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path

from dbt_config_guard.formatters.formatter import Formatter

def _import_formatter_classes() -> dict[str, type[Formatter]]:
    formatter_classes: dict[str, type[Formatter]] = {}
    for module_info in pkgutil.iter_modules([
        Path(__file__).parent.resolve().as_posix(),
    ]):
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if not inspect.isclass(attribute):
                continue

            if not issubclass(attribute, Formatter):
                continue

            if inspect.isabstract(attribute):
                continue

            formatter_classes[module_info.name] = attribute

    return formatter_classes

FORMATTER_CLASSES = _import_formatter_classes()
