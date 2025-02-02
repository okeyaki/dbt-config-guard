from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.entities.entity import Entity

if TYPE_CHECKING:
    from pathlib import Path

    from ruamel.yaml import CommentedMap

class Project(Entity):
    CONFIG_FILE_NAME = "dbt_project.yml"

    def __init__(
        self,
        *,
        config: CommentedMap,
        dir_path: Path,
    ) -> None:
        super().__init__(
            config=config,
        )

        self._dir_path = dir_path

    @property
    def config_file_path(self) -> Path:
        return self._dir_path / self.CONFIG_FILE_NAME

    @property
    def dir_path(self) -> Path:
        return self._dir_path

    @property
    def id(self) -> str:
        return f"project:{self.name}"

    @property
    def model_dir_paths(self) -> list[Path]:
        return [
            self._dir_path / e
            for e
            in self._config.get("model-paths", [])
        ]

    @property
    def source_dir_paths(self) -> list[Path]:
        return [
            self._dir_path / e
            for e
            in self._config.get("model-paths", [])
        ]
