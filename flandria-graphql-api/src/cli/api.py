import os

import click
from strawberry.cli.utils import load_schema
from strawberry.printer import print_schema
from uvicorn import run

from src.api._codegen import (
    generate_strawberry_input_filters,
    generate_strawberry_models,
    generate_strawberry_sort_inputs,
)
from src.core.utils import run_ruff


@click.group(name="api")
def api_cli():
    pass


@api_cli.command("debug")
def api_run_debug():
    run("src.api.app:app", host="0.0.0.0", reload=True)


@api_cli.command("export-schema")
@click.argument("export_path", type=click.STRING)
def export_schema(export_path: str):
    # taken from strawberry/cli/commands/export_schema.py
    schema_symbol = load_schema("src.api.schema:schema", ".")
    schema_text = print_schema(schema_symbol)

    with open(export_path, "w") as fp:
        fp.write(schema_text)


@api_cli.group("codegen", chain=True)
def codegen():
    pass


@codegen.command("models")
def generate_models():
    dst_path = os.path.join("src", "api", "types", "_generated.py")

    with open(dst_path, "w", encoding="utf-8") as fp:
        fp.write(generate_strawberry_models())

    run_ruff(dst_path)


@codegen.command("filters")
def generate_filters():
    dst_path = os.path.join("src", "api", "inputs", "filters", "_generated.py")

    with open(dst_path, "w", encoding="utf-8") as fp:
        fp.write(generate_strawberry_input_filters())

    run_ruff(dst_path)


@codegen.command("sorts")
def generate_sorts():
    dst_path = os.path.join("src", "api", "inputs", "sort", "_generated.py")

    with open(dst_path, "w", encoding="utf-8") as fp:
        fp.write(generate_strawberry_sort_inputs())

    run_ruff(dst_path)
