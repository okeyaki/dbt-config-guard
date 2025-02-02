from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.entities.entity import Entity

if TYPE_CHECKING:
    from pathlib import Path

    from ruamel.yaml import CommentedMap

    from dbt_config_guard.entities.project import Project

class Model(Entity):
    def __init__(
        self,
        *,
        config: CommentedMap,
        config_file_path: Path,
        project: Project,
    ) -> None:
        super().__init__(
            config=config,
        )

        self._config_file_path = config_file_path
        self._project = project

    def __str__(self) -> str:
        return ""

    @property
    def config_file_path(self) -> Path:
        return self._config_file_path

    @property
    def project(self) -> Project:
        return self._project

    @property
    def id(self) -> str:
        return f"model:{self.name}"

    @property
    def column_configs(self) -> list[CommentedMap]:
        return self.config.get("columns", [])
