from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.entities.model import Model
from dbt_config_guard.entities.model_column import ModelColumn
from dbt_config_guard.entities.project import Project
from dbt_config_guard.entities.source import Source
from dbt_config_guard.entities.source_column import SourceColumn
from dbt_config_guard.rules import RULE_CLASSES
from dbt_config_guard.rules.model import ModelRule
from dbt_config_guard.rules.model_column import ModelColumnRule
from dbt_config_guard.rules.project import ProjectRule
from dbt_config_guard.rules.source import SourceRule
from dbt_config_guard.rules.source_column import SourceColumnRule
from dbt_config_guard.services.registry import Registry
from dbt_config_guard.services.ruleset import Ruleset

if TYPE_CHECKING:
   from collections.abc import Generator
   from pathlib import Path

   from dbt_config_guard.violations.violation import Violation

class Checker:
    def __init__(
        self,
        *,
        config: dict,
        project_dir_path: Path,
    ) -> None:
        self._config = config
        self._project_dir_path = project_dir_path

        self._registry = Registry(
            project_dir_path=project_dir_path,
        )

    def run(self) -> Generator[Violation, None, None]:
        yield from self._check_project(self._config)
        yield from self._check_models(self._config)
        yield from self._check_model_columns(self._config)
        yield from self._check_sources(self._config)
        yield from self._check_source_columns(self._config)

    def _check_project(self, config: dict) -> Generator[Violation, None, None]:
        project_ruleset = Ruleset[Project].from_config(
            rule_classes=[e for e in RULE_CLASSES.values() if issubclass(e, ProjectRule)],
            config=config,
        )
        yield from project_ruleset.check(self._registry.find_project(), self._registry)

    def _check_models(self, config: dict) -> Generator[Violation, None, None]:
        model_ruleset = Ruleset[Model].from_config(
            rule_classes=[e for e in RULE_CLASSES.values() if issubclass(e, ModelRule)],
            config=config,
        )
        for model in self._registry.find_models():
            yield from model_ruleset.check(model, self._registry)

    def _check_model_columns(self, config: dict) -> Generator[Violation, None, None]:
        model_column_ruleset = Ruleset[ModelColumn].from_config(
            rule_classes=[e for e in RULE_CLASSES.values() if issubclass(e, ModelColumnRule)],
            config=config,
        )
        for model_column in self._registry.find_model_columns():
            yield from model_column_ruleset.check(model_column, self._registry)

    def _check_sources(self, config: dict) -> Generator[Violation, None, None]:
        source_ruleset = Ruleset[Source].from_config(
            rule_classes=[e for e in RULE_CLASSES.values() if issubclass(e, SourceRule)],
            config=config,
        )
        for source in self._registry.find_sources():
            yield from source_ruleset.check(source, self._registry)

    def _check_source_columns(self, config: dict) -> Generator[Violation, None, None]:
        source_column_ruleset = Ruleset[SourceColumn].from_config(
            rule_classes=[e for e in RULE_CLASSES.values() if issubclass(e, SourceColumnRule)],
            config=config,
        )
        for source_column in self._registry.find_source_columns():
            yield from source_column_ruleset.check(source_column, self._registry)
