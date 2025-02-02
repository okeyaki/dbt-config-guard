from __future__ import annotations

from typing import TYPE_CHECKING

from dbt_config_guard.entities.entity import Entity
from dbt_config_guard.errors.logic import LogicError

if TYPE_CHECKING:
    from pathlib import Path

    from ruamel.yaml import CommentedMap

    from dbt_config_guard.entities.model import Model

class ModelColumn(Entity):
    def __init__(
        self,
        *,
        config: CommentedMap,
        model: Model,
    ) -> None:
        super().__init__(
            config=config,
        )

        self._model = model

    @property
    def config_file_path(self) -> Path:
        return self.model.config_file_path

    @property
    def model(self) -> Model:
        return self._model

    @property
    def id(self) -> str:
        return f"model:{self.model.name}.{self.name}"

    @property
    def data_type(self) -> str:
        return self.config.get("data_type", "")

    def has_same_name(self, rhs: ModelColumn) -> bool:
        return self.name == rhs.name

    def has_same_description(self, rhs: ModelColumn) -> bool:
        return self.description == rhs.description

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
