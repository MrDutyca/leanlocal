"""Small, read-only system checks with privacy-safe defaults."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def _os_name() -> str:
    path = Path("/etc/os-release")
    if not path.exists():
        return platform.system()
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("PRETTY_NAME="):
            return line.split("=", 1)[1].strip().strip('"')
    return platform.system()


def _memory_bytes() -> int:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return 0


def report() -> dict:
    """Return a deliberately non-identifying capability summary."""
    total, used, free = shutil.disk_usage("/")
    return {
        "os": _os_name(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "logical_cpus": os.cpu_count() or 1,
        "memory_gib": round(_memory_bytes() / (1024 ** 3), 2),
        "disk_total_gib": round(total / (1024 ** 3), 1),
        "disk_free_gib": round(free / (1024 ** 3), 1),
    }


def _command_version(command: str) -> dict:
    path = shutil.which(command)
    if not path:
        return {"present": False}
    try:
        proc = subprocess.run(
            [command, "--version"],
            text=True,
            capture_output=True,
            timeout=3,
            check=False,
        )
        text = (proc.stdout or proc.stderr).splitlines()[0][:120]
    except (OSError, subprocess.SubprocessError, IndexError):
        text = ""
    return {"present": True, "version": text}


def check() -> dict:
    """Read-only checks for common lightweight local tools."""
    return {name: _command_version(name) for name in ("python3", "git", "curl")}


def fit() -> dict:
    """Conservative, generic guidance based only on CPU count and RAM."""
    data = report()
    ram = data["memory_gib"]
    cpus = data["logical_cpus"]
    if ram < 4:
        level = "very-light"
        note = "Prefer command-line tools and small single-purpose workloads."
    elif ram < 8 or cpus < 4:
        level = "light"
        note = "Suitable for lightweight local tools; avoid memory-heavy workloads."
    elif ram < 16:
        level = "moderate"
        note = "Suitable for many lightweight local workloads with sensible limits."
    else:
        level = "roomier"
        note = "More headroom is available, but workload limits still matter."
    return {"class": level, "guidance": note}


def _mb_per_second(size_bytes: int, seconds: float) -> float:
    if seconds <= 0:
        return 0.0
    return round((size_bytes / (1024 ** 2)) / seconds, 1)


def bench() -> dict:
    """Run deliberately short, low-resource local checks."""
    start = time.perf_counter()
    digest = b"leanlocal"
    for _ in range(120_000):
        digest = hashlib.sha256(digest).digest()
    cpu_seconds = round(time.perf_counter() - start, 3)

    size = 8 * 1024 * 1024
    source = bytearray(size)
    start = time.perf_counter()
    target = source[:]
    memory_mbps = _mb_per_second(len(target), time.perf_counter() - start)

    block = b"\0" * (1024 * 1024)
    start = time.perf_counter()
    with tempfile.TemporaryFile() as handle:
        for _ in range(4):
            handle.write(block)
        handle.flush()
        os.fsync(handle.fileno())
    storage_mbps = _mb_per_second(4 * len(block), time.perf_counter() - start)

    return {
        "cpu_sha256_seconds": cpu_seconds,
        "memory_copy_mib_s": memory_mbps,
        "temp_storage_write_mib_s": storage_mbps,
    }


def support_bundle(path: str) -> str:
    payload = {"report": report(), "check": check(), "fit": fit()}
    Path(path).write_text(json.dumps(payload, indent=2) + "\n")
    return path
