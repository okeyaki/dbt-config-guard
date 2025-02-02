from __future__ import annotations

from typing import TYPE_CHECKING

from ruamel.yaml import YAML

from dbt_config_guard.entities.model import Model
from dbt_config_guard.entities.model_column import ModelColumn
from dbt_config_guard.entities.project import Project
from dbt_config_guard.entities.source import Source
from dbt_config_guard.entities.source_column import SourceColumn

if TYPE_CHECKING:
    from pathlib import Path

class Registry:
    def __init__(
        self,
        *,
        project_dir_path: Path,
    ) -> None:
        self._project_dir_path = project_dir_path

        self._project: Project | None = None
        self._models: list[Model] | None = None
        self._model_columns: dict[Model, list[ModelColumn]] = {}
        self._sources: list[Source] | None = None
        self._source_columns: dict[Source, list[SourceColumn]] = {}

    def find_project(self) -> Project:
        if self._project is None:
            self._project = self._load_project()

        return self._project

    def find_models(self) -> list[Model]:
        if self._models is None:
            self._models = self._load_models()

        return self._models

    def find_model_columns(self) -> list[ModelColumn]:
        model_columns: list[ModelColumn] = []
        for model in self.find_models():
            model_columns.extend(self.find_model_columns_by_model(model))

        return model_columns

    def find_model_columns_by_model(self, model: Model) -> list[ModelColumn]:
        if model not in self._model_columns:
            self._model_columns[model] = self._load_model_columns(model)

        return self._model_columns[model]

    def find_model_columns_by_name(self, model_column_name: str) -> list[ModelColumn]:
        return [
            e
            for e
            in self.find_model_columns()
            if e.name == model_column_name
        ]

    def find_sources(self) -> list[Source]:
        if self._sources is None:
            self._sources = self._load_sources()

        return self._sources

    def find_source_columns(self) -> list[SourceColumn]:
        source_columns: list[SourceColumn] = []
        for source in self.find_sources():
            source_columns.extend(self.find_source_columns_by_source(source))

        return source_columns

    def find_source_columns_by_source(self, source: Source) -> list[SourceColumn]:
        if source not in self._source_columns:
            self._source_columns[source] = self._load_source_columns(source)

        return self._source_columns[source]

    def _load_project(self) -> Project:
        return Project(
            dir_path=self._project_dir_path,
            config=YAML().load(self._project_dir_path / Project.CONFIG_FILE_NAME),
        )

    def _load_models(self) -> list[Model]:
        project = self.find_project()

        models: list[Model] = []
        for model_dir_path in project.model_dir_paths:
            for file_path in model_dir_path.glob("**/*.yml"):
                if file_path.is_dir():
                    continue

                file_content = YAML().load(file_path)

                if "models" not in file_content:
                    continue

                for model_config in file_content.get("models", []):
                    models.append(Model(
                        config=model_config,
                        project=project,
                        config_file_path=file_path,
                    ))

        return models

    def _load_model_columns(self, model: Model) -> list[ModelColumn]:
        return [
            ModelColumn(
                config=e,
                model=model,
            )
            for e
            in model.config.get("columns", [])
        ]

    def _load_sources(self) -> list[Source]:
        project = self.find_project()

        sources: list[Source] = []
        for source_dir_path in project.source_dir_paths:
            for file_path in source_dir_path.glob("**/*.yml"):
                if file_path.is_dir():
                    continue

                file_content = YAML().load(file_path)

                if "sources" not in file_content:
                    continue

                for source_config in file_content.get("sources", []):
                    sources.append(Source(
                        config=source_config,
                        project=project,
                        config_file_path=file_path,
                    ))

        return sources

    def _load_source_columns(self, source: Source) -> list[SourceColumn]:
        return [
            SourceColumn(
                config=e,
                source=source,
            )
            for e
            in source.config.get("columns", [])
        ]
