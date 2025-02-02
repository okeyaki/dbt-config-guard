from __future__ import annotations

from pathlib import Path

import click

from dbt_config_guard.formatters import FORMATTER_CLASSES
from dbt_config_guard.services.checker import Checker
from dbt_config_guard.utils.config import ConfigUtils

@click.command(
    name="check",
)
@click.option(
    "--output-format-type",
    "-o",
    "output_format_type",
    type=click.Choice(list(FORMATTER_CLASSES.keys())),
    default="text",
)
def check(
    output_format_type: str,
) -> None:
    checker = Checker(
        project_dir_path=Path("etc/dbt/examples/jaffle-shop"),
        config=ConfigUtils.load(),
    )

    formatter = FORMATTER_CLASSES[output_format_type]()
    for violation in checker.run():
        click.echo(formatter.format(violation))
