import os
import shutil
import subprocess
import typing as t
from pathlib import Path

DEFAULT_BIN_DIR = Path.home().joinpath("nats-server").absolute()


def get_executable(bin_name: str = "nats-server") -> str:
    """Get path to nats-server executable"""
    # User directory
    if DEFAULT_BIN_DIR.joinpath(bin_name).is_file():
        return DEFAULT_BIN_DIR.joinpath(bin_name).as_posix()
    elif DEFAULT_BIN_DIR.joinpath(bin_name + ".exe").is_file():
        return DEFAULT_BIN_DIR.joinpath(bin_name + ".exe").as_posix()
    # Any directory within PATH
    else:
        path = shutil.which(bin_name)
        if path is None:
            raise FileNotFoundError("nats-server executable not found")
        return path


def nats_server(
    *args: str,
    stdout: t.Optional[t.Any] = None,
    stderr: t.Optional[t.Any] = None,
    max_cpus: t.Optional[int] = None,
    executable: t.Optional[str] = None,
) -> "subprocess.Popen[bytes]":
    """Execute NATS server using subprocess.Popen"""
    executable = executable or get_executable("nats-server")
    args = (executable,) + args
    env = os.environ.copy()
    if max_cpus:
        env["GOMAXPROCS"] = format(max_cpus, ".2f")
    return subprocess.Popen(args, stdout=stdout, stderr=stderr, env=env)
