from __future__ import annotations

from ruamel.yaml import CommentedMap

from dbt_config_guard.entities.source_column import SourceColumn

from test.fixtures.fixture import Fixture
from test.fixtures.source import SourceFixture

class SourceColumnFixture(Fixture[SourceColumn]):
    @classmethod
    def with_defaults(cls) -> SourceColumnFixture:
        return SourceColumnFixture(
            name="customer_id",
            description = "the customer id",
            data_tests=[
                "unique",
                "not_null",
                {
                    "dbt_utils.not_empty_string": {
                      "trim_whitespace": False,
                    },
                },
            ],
            source=SourceFixture.with_defaults(),
        )

    def __init__(
        self,
        *,
        name: str,
        description: str,
        data_tests: list[str | dict],
        source: SourceFixture,
    ) -> None:
        self.name = name
        self.description = description
        self.data_tests = data_tests
        self.source = source

    def _build(self) -> SourceColumn:
        return SourceColumn(
            config=CommentedMap(
                name=self.name,
                description=self.description,
                data_tests=self.data_tests,
            ),
            source=self.source.create(),
        )
