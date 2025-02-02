from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.entities.entity import Entity
from dbt_config_guard.errors.logic import LogicError

if TYPE_CHECKING:
    from pathlib import Path

    from ruamel.yaml import CommentedMap

    from dbt_config_guard.entities.source import Source

class SourceColumn(Entity):
    def __init__(
        self,
        *,
        config: CommentedMap,
        source: Source,
    ) -> None:
        super().__init__(
            config=config,
        )

        self._source = source

    @property
    def config_file_path(self) -> Path:
        return self.source.config_file_path

    @property
    def source(self) -> Source:
        return self._source

    @property
    def id(self) -> str:
        return f"source:{self.source.name}.{self.name}"

    @property
    def data_type(self) -> str:
        return self.config.get("data_type", "")

    def has_data_test(self, data_test_name: str) -> bool:
        for data_test in self.config.get("data_tests", []):
            if isinstance(data_test, str):
                if data_test == data_test_name:
                    return True

                continue

            if isinstance(data_test, dict):
                if data_test_name in data_test:
                    return True

                continue

            raise LogicError

        return False
