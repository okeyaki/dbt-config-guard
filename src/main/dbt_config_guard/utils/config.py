from __future__ import annotations

from pathlib import Path

from ruamel.yaml import CommentedMap
from ruamel.yaml import YAML

from dbt_config_guard.services.ruleset import Ruleset

class ConfigUtils:
    DEFAULT_CONFIG_FILE_NAME = ".dbt_config_guard.yml"

    @classmethod
    def default_config(cls) -> CommentedMap:
        return Ruleset.default_config()

    @classmethod
    def load(cls, config_file_name: str | None = None) -> CommentedMap:
        if config_file_name is None:
            config_file_name = cls.DEFAULT_CONFIG_FILE_NAME

        config_file_path = Path(config_file_name)

        if config_file_path.exists():
            return YAML().load(Path(config_file_name))

        return cls.default_config()
