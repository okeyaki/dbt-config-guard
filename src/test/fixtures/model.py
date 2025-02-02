from __future__ import annotations

from pathlib import Path

from ruamel.yaml import CommentedMap

from dbt_config_guard.entities.model import Model

from test.fixtures.fixture import Fixture
from test.fixtures.project import ProjectFixture

class ModelFixture(Fixture[Model]):
    @classmethod
    def with_defaults(cls) -> ModelFixture:
        return ModelFixture(
            name="mart__customers",
            config_file_path=Path("/jaffle-shop/models/marts/mart__customers.yml"),
            project=ProjectFixture.with_defaults(),
        )

    def __init__(
        self,
        *,
        name: str,
        config_file_path: Path,
        project: ProjectFixture,
    ) -> None:
        self.name = name
        self.config_file_path = config_file_path
        self.project = project

    def _build(self) -> Model:
        return Model(
            config=CommentedMap(
                name=self.name,
            ),
            config_file_path=self.config_file_path,
            project=self.project.create(),
        )
