import os
import shutil
import signal
import subprocess
import tempfile
import time
import types
import typing as t
import warnings
import weakref
from enum import Enum
from pathlib import Path

import httpx

from .cmd import nats_server
from .config import ConfigGenerator, ServerOptions
from .monitor import NATSMonitor


class Signal(str, Enum):
    KILL = "KILL"
    QUIT = "QUIT"
    STOP = "STOP"
    REOPEN = "REOPEN"
    RELOAD = "RELOAD"
    LDM = "LDM"


class NATSD:
    def __init__(
        self,
        options: t.Optional[ServerOptions] = None,
        max_cpus: t.Optional[int] = None,
        config_file: t.Optional[str] = None,
        store_dir: t.Optional[str] = None,
        redirect_output: bool = False,
        start_timeout: float = 5,
        stop_timeout: float = 15,
    ) -> None:
        """Create a new instance of nats-server daemon."""
        # Whether to redirect stdout/stderr
        self.redirect_output = redirect_output
        # Store timeout
        self.start_timeout = start_timeout
        self.stop_timeout = stop_timeout
        # Store options
        self.options = options or ServerOptions()
        # Store max CPU
        self.max_cpus = max_cpus
        # Extract monitoring endpoint
        http_base_path = self.options.http_base_path or "/"
        if not (
            self.options.http
            or self.options.http_port
            or self.options.https_port
            or self.options.https
        ):
            self.options.http = "127.0.0.1:8222"
            self.monitoring_endpoint = f"http://{self.options.http}{http_base_path}"
        elif self.options.http_port:
            self.monitoring_endpoint = (
                f"http://127.0.0.1:{self.options.http_port}{http_base_path}"
            )
        elif self.options.http:
            self.monitoring_endpoint = f"http://{self.options.http}{http_base_path}"
        else:
            raise NotImplementedError(
                "NATSD instances cannot be created with TLS enabled monitoring endpoint"
            )
        # Generate config
        generator = ConfigGenerator()
        config_str = generator.render(self.options)
        # Determine path to config file
        if config_file is None:
            self.config_file = Path(tempfile.mkdtemp()).joinpath("nats.conf")
            weakref.finalize(self, shutil.rmtree, self.config_file.parent, True)
        else:
            self.config_file = Path(config_file).expanduser().absolute()
        # Write config to file
        self.config_file.write_text(config_str)
        # Check is store dir was provided or needs to be created
        if self.options.jetstream:
            if self.options.jetstream.store_dir is None and store_dir is None:
                self.options.jetstream.store_dir = tempfile.mkdtemp()
                # Clean-up temporary store dir on exit
                weakref.finalize(
                    self, shutil.rmtree, self.options.jetstream.store_dir, True
                )
        # Initialize subprocess attribute
        self.proc: t.Optional["subprocess.Popen[bytes]"] = None
        # Create a monitor instance
        self.monitor = NATSMonitor(self.monitoring_endpoint)

    def is_alive(self) -> bool:
        if self.proc is None:
            return False
        return self.proc.poll() is None

    def _cleanup_on_exit(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.kill()

    def start(self, wait: bool = False) -> "NATSD":
        """Start NATS server."""
        if self.redirect_output:
            self.proc = nats_server(
                "--config",
                self.config_file.as_posix(),
                max_cpus=self.max_cpus,
                stdout=None,
                stderr=None,
            )
        else:
            self.proc = nats_server(
                "--config",
                self.config_file.as_posix(),
                max_cpus=self.max_cpus,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        if wait:
            deadline = time.time() + self.start_timeout or float("inf")
            while True:
                status = self.proc.poll()
                if status is not None:
                    raise subprocess.CalledProcessError(
                        returncode=self.proc.returncode, cmd=self.proc.args
                    )
                if time.time() > deadline:
                    self.stop()
                    raise TimeoutError(
                        f"nats-server failed to start before timeout ({self.start_timeout:.3f}s)"
                    )
                try:
                    self.monitor.varz()
                    break
                except httpx.HTTPError as exc:
                    print(
                        f"DEBUG: Waiting for server to be up. Last error: {type(exc).__name__} - {repr(exc)}."
                    )
                    time.sleep(0.1)
                    continue

        weakref.finalize(self, self._cleanup_on_exit)
        return self

    def stop(self, timeout: t.Optional[float] = None) -> None:
        if self.proc is None:
            return
        if self.proc.poll() is not None:
            return
        else:
            try:
                self.term(timeout=timeout or self.stop_timeout)
            except TimeoutError:
                self.kill()
        expected = 15 if os.name == "nt" else 1
        if self.proc and self.proc.returncode != expected:
            raise subprocess.CalledProcessError(
                self.proc.returncode, cmd=self.proc.args
            )

    def wait(self, timeout: t.Optional[float] = None) -> int:
        """Wait for process to finish and return status code.

        Possible status codes on Linux (non-exhaustive):
            -1: process is not started yet.
            0: process has been stopped after entering lame duck mode.
            1: process has been stopped due to TERM signal.
            2: process has been stopped due to QUIT signal.
            -9: process has been stopped due to KILL signal.
        """
        if self.proc is None:
            return 0
        status = self.proc.poll()
        if status is not None:
            return status
        return self.proc.wait(timeout=timeout)

    def quit(self, timeout: t.Optional[float] = None) -> None:
        """Send signal to immediately kill process with a core dump and wait until process exits."""
        self.send_signal(Signal.QUIT)
        self.wait(timeout=timeout or self.stop_timeout)

    def kill(self, timeout: t.Optional[float] = None) -> None:
        """Send signal to immediately kill process and wait until process exits."""
        self.send_signal(Signal.KILL)
        self.wait(timeout=timeout or self.stop_timeout)

    def term(self, timeout: t.Optional[float] = None) -> None:
        """Send signal to gracefully terminate process and wait until process exits."""
        self.send_signal(Signal.STOP)
        self.wait(timeout=timeout or self.stop_timeout)

    def reopen_log_file(self) -> None:
        """Send signal to reopen log file.

        NOTE: Not supported on Windows except when running nats-server as a service
        """
        self.send_signal(Signal.REOPEN)

    def enter_lame_duck_mode(self) -> None:
        """Send signal to enter Lame Duck Mode.

        NOTE: Not supported on Windows except when running nats-server as a service
        """
        self.send_signal(Signal.LDM)

    def reload_config(self) -> None:
        """Send signal to reload config.

        NOTE: Not supported on Windows except when running nats-server as a service
        """
        self.send_signal(Signal.RELOAD)

    def __enter__(self) -> "NATSD":
        return self.start(wait=True)

    def __exit__(
        self,
        error_type: t.Optional[t.Type[BaseException]] = None,
        error: t.Optional[BaseException] = None,
        traceback: t.Optional[types.TracebackType] = None,
    ) -> None:
        self.stop()

    def _send_signal_unix(self, _signal: Signal) -> None:
        if os.name != "nt" and self.proc and self.proc.poll() is None:
            if _signal == Signal.KILL:
                # Kill the process immediatley
                sig = signal.SIGKILL
            elif _signal == Signal.QUIT:
                # Kills the process immediately and perform a core dump
                sig = signal.SIGQUIT
            elif _signal == Signal.STOP:
                # Stops the server grafefully
                sig = signal.SIGTERM
            elif _signal == Signal.REOPEN:
                # Reopens the log file for log rotation
                sig = signal.SIGUSR1
            elif _signal == Signal.RELOAD:
                # Reload server configuration
                sig = signal.SIGHUP
            elif _signal == Signal.LDM:
                # Stops the server after evicting all clients
                sig = signal.SIGUSR2
            os.kill(self.proc.pid, sig.value)

    def _send_signal_windows(self, _signal: Signal) -> None:
        if os.name == "nt" and self.proc and self.proc.poll() is None:
            if _signal == Signal.KILL or _signal == Signal.QUIT:
                warnings.warn(
                    "Quit and Kill are not supported on Windows. Interrupting process."
                )
                os.kill(self.proc.pid, signal.SIGINT)
            elif _signal == Signal.STOP:
                os.kill(self.proc.pid, signal.SIGINT)
            elif _signal == Signal.RELOAD:
                warnings.warn("Log file roration is not supported on Windows")
            elif _signal == Signal.REOPEN:
                warnings.warn("Config reload is not supported on Windows")
            elif _signal == Signal.LDM:
                warnings.warn(
                    "Lame Duck Mode is not supported on Windows. Interrupting process."
                )
                os.kill(self.proc.pid, signal.SIGINT)

    def send_signal(self, _signal: Signal) -> None:
        """Send a signal to nats-server. Not well supported on Windows."""
        _signal = Signal(_signal)
        if self.proc is None:
            raise TypeError("Process is not started yet")
        status = self.proc.poll()
        if status is not None:
            raise subprocess.CalledProcessError(status, cmd=self.proc.args)
        if os.name != "nt":
            self._send_signal_unix(_signal)
        else:
            self._send_signal_windows(_signal)
