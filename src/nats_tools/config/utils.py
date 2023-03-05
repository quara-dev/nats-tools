import subprocess
import tempfile
import typing as t
from dataclasses import asdict, is_dataclass
from pathlib import Path

import jinja2

from ..cmd import nats_server
from ..errors import InvalidConfigError


def check_config(config: str) -> None:
    with tempfile.TemporaryDirectory(prefix="nats_tools_", suffix="-") as tempdir:
        config_file = Path(tempdir) / "nats.conf"
        config_file.write_text(config)
        process = nats_server(
            "--config",
            config_file.as_posix(),
            "-t",
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        stderr: bytes
        _, stderr = process.communicate()
        if process.returncode != 0:
            error = error = (
                stderr.split(b"nats-server:", maxsplit=1)[1].strip().decode()
            )
            error_config_file = config_file.parent.parent.joinpath(
                tempdir + "nats.conf"
            )
            error_config_file.write_text(config)
            if config_file.as_posix() in error:
                error = error.replace(
                    config_file.as_posix(), error_config_file.as_posix()
                )
            else:
                error = f"({error_config_file.as_posix()}) {error}"
            raise InvalidConfigError(error)


def non_null(values: t.Any) -> t.Any:
    """Get a dictionary out of a dataclass"""
    if is_dataclass(values):
        values = asdict(values)
    if isinstance(values, dict):
        for k, v in values.copy().items():
            if v is None:
                values.pop(k)
            else:
                values[k] = non_null(v)
    elif isinstance(values, list):
        for idx, value in enumerate(values.copy()):
            values[idx] = non_null(value)
    return values


def load_template_from_path(template: t.Union[str, Path]) -> jinja2.Template:
    """Load a jinja2 template from path."""
    filepath = Path(template).absolute()
    if not filepath.exists():
        raise FileNotFoundError(filepath.as_posix())
    loader = jinja2.FileSystemLoader(filepath.parent)
    environment = jinja2.Environment(loader=loader, autoescape=False)
    return environment.get_template(filepath.name)


def load_template_from_name(template: str) -> jinja2.Template:
    """Load a jinja2 template from name."""
    loader = jinja2.FileSystemLoader(Path(__file__).parent.joinpath("templates"))
    environment = jinja2.Environment(loader=loader, autoescape=True)
    return environment.get_template(template)
