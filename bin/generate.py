#!/usr/bin/env python

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader

from dbt_config_guard.rules import RULE_CLASSES
from dbt_config_guard.utils.text import TextUtils

_OUTPUT_DIR_PATH = Path("doc/rules")
_TEMPLATE_DIR_PATH = Path("etc/jinja2/templates")

def generate_rule_index(env: Environment) -> None:
    template = env.get_template("rule_index.md.j2")

    file_path = _OUTPUT_DIR_PATH / "README.md"
    with file_path.open("w") as f:
        f.write(template.render(
            rule_classes=RULE_CLASSES,
        ))

def generate_rule_item(env: Environment) -> None:
    template = env.get_template("rule_item.md.j2")
    for rule_class in RULE_CLASSES.values():
        rule_schema = rule_class.schema()

        file_path = _OUTPUT_DIR_PATH / f"{rule_schema.name}.md"
        with file_path.open("w") as f:
            f.write(template.render(
                rule_schema=rule_schema,
            ))

def main() -> None:
    for file_path in _OUTPUT_DIR_PATH.glob("*"):
        file_path.unlink()

    env = Environment(
        autoescape=True,
        keep_trailing_newline=True,
        loader=FileSystemLoader(_TEMPLATE_DIR_PATH),
    )

    env.filters["dedent"] = TextUtils.dedent

    generate_rule_index(env)

    generate_rule_item(env)

if __name__ == "__main__":
    main()
