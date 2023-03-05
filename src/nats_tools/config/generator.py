import typing as t
from dataclasses import dataclass
from pathlib import Path

from .options import ServerOptions
from .utils import (
    check_config,
    load_template_from_name,
    load_template_from_path,
    non_null,
)


@dataclass
class GeneratorContext:
    salt: t.Optional[bytes] = None

    @classmethod
    def new(cls) -> "GeneratorContext":
        ctx = cls()
        return ctx


class ConfigGenerator:
    def __init__(
        self,
        template: t.Union[str, Path] = "default.j2",
        context: t.Optional[GeneratorContext] = None,
    ) -> None:
        """Create a new instance of config generator.

        Arguments:
            template: the template used to render configuration.
        """
        self.context = context or GeneratorContext.new()
        if isinstance(template, Path):
            self.template = load_template_from_path(template)
        elif Path(template).is_file():
            self.template = load_template_from_path(template)
        else:
            self.template = load_template_from_name(template)

    def render(
        self,
        options: ServerOptions,
        check: bool = True,
    ) -> str:
        """Render configuration according to arguments."""
        if options.leafnodes and options.leafnodes.listen:
            options.leafnodes.host = None
            options.leafnodes.port = None
        values = non_null(options)
        if options.server_tags:
            values["server_tags"] = [
                ":".join([key, value]) for key, value in options.server_tags.items()
            ]
        config = self.template.render(values)
        config = config.replace(r"\u003e", ">")
        if check:
            check_config(config)
        return config


def render(options: ServerOptions, template: t.Union[str, Path, None] = None) -> str:
    """Render a config from options.

    If you plan to use this function several times, prefer using
    ConfigGenerator instance instead.
    """
    opts: t.Dict[str, t.Any] = {}
    if template:
        opts["template"] = template
    generator = ConfigGenerator(**opts)
    return generator.render(options)
