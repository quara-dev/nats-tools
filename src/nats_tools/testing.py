import typing as t

import pytest
from _pytest.fixtures import SubRequest

from nats_tools.natsd import NATSD, ServerOptions

F = t.TypeVar("F", bound=t.Callable[..., t.Any])


@pytest.fixture
def natsd(request: SubRequest) -> t.Iterator[NATSD]:
    if hasattr(request, "param"):
        options: ServerOptions = request.param
    else:
        options = ServerOptions()
    if options.debug is None:
        options.debug = True
    if options.trace is None:
        options.trace = True
    with NATSD(options) as daemon:
        yield daemon


def parametrize_nats_server(options: ServerOptions) -> t.Callable[[F], F]:
    return pytest.mark.parametrize("natsd", [options], indirect=True)
