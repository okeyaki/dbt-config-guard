from __future__ import annotations

from ruamel.yaml import CommentedMap

from dbt_config_guard.entities.model_column import ModelColumn

from test.fixtures.fixture import Fixture
from test.fixtures.model import ModelFixture

class ModelColumnFixture(Fixture[ModelColumn]):
    @classmethod
    def with_defaults(cls) -> ModelColumnFixture:
        return ModelColumnFixture(
            name="customer_id",
            description="the customer id",
            data_tests=[
                "unique",
                "not_null",
                {
                    "dbt_utils.not_empty_string": {
                      "trim_whitespace": False,
                    },
                },
            ],
            model=ModelFixture.with_defaults(),
        )

    def __init__(
        self,
        *,
        name: str,
        description: str,
        data_tests: list[str | dict],
        model: ModelFixture,
    ) -> None:
        self.name = name
        self.description = description
        self.data_tests = data_tests
        self.model = model

    def _build(self) -> ModelColumn:
        return ModelColumn(
            config=CommentedMap(
                name=self.name,
                description=self.description,
                data_tests=self.data_tests,
            ),
            model=self.model.create(),
        )
