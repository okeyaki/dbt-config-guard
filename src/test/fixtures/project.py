from __future__ import annotations

from pathlib import Path

from ruamel.yaml import CommentedMap

from dbt_config_guard.entities.project import Project

from test.fixtures.fixture import Fixture

class ProjectFixture(Fixture[Project]):
    @classmethod
    def with_defaults(cls) -> ProjectFixture:
        return ProjectFixture(
            name="jaffle_shop",
            dir_path=Path("/jaffle-shop"),
        )

    def __init__(
        self,
        *,
        name: str,
        dir_path: Path,
    ) -> None:
        self.name = name
        self.dir_path = dir_path

    def _build(self) -> Project:
        return Project(
            config=CommentedMap(
                name=self.name,
            ),
            dir_path=self.dir_path,
        )
