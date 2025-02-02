from __future__ import annotations

import click

from dbt_config_guard.commands.check import check

def main() -> None:
    _main()


@click.group()
def _main() -> None:
    pass


_main.add_command(check)
