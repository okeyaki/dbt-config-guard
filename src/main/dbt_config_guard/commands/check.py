from __future__ import annotations

from pathlib import Path

import click

from dbt_config_guard.services.checker import Checker
from dbt_config_guard.utils.config import ConfigUtils

@click.command(
    name="check",
)
def check() -> None:
    checker = Checker(
        project_dir_path=Path("etc/dbt/examples/jaffle-shop"),
        config=ConfigUtils.load(),
    )

    for violation in checker.run():
        click.echo(violation)
