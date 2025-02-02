from __future__ import annotations

from pathlib import Path

from ruamel.yaml import CommentedMap

from dbt_config_guard.entities.source import Source

from test.fixtures.fixture import Fixture
from test.fixtures.project import ProjectFixture

class SourceFixture(Fixture[Source]):
    @classmethod
    def with_defaults(cls) -> SourceFixture:
        return SourceFixture(
            name="customers",
            config_file_path=Path("/jaffle-shop/models/sources/customers.yml"),
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

    def _build(self) -> Source:
        return Source(
            config=CommentedMap(
                name=self.name,
            ),
            config_file_path=Path(self.config_file_path),
            project=self.project.create(),
        )
