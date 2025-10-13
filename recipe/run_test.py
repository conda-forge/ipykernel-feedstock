import json
import os
import platform
import sys
import pytest
import typing
from pathlib import Path

# TODO: investigate upstream interrupt regression in 6.5.0
test_skips = ["flaky", "interrupt"]

py_major = sys.version_info[0]
py_impl = platform.python_implementation().lower()
machine = platform.machine().lower()
system = platform.system().lower()

is_aarch = "aarch64" in machine
is_ppc = "ppc" in machine
is_pypy = py_impl == "pypy"
is_win = system == "windows"

prefix = Path(os.environ["PREFIX"])


def check_kernel() -> int:
    print(f"Python implementation: {py_impl}")
    print(f"              Machine: {machine}")
    print(f"               System: {system}")

    specfile = prefix / f"share/jupyter/kernels/python{py_major}/kernel.json"

    print(f"Checking Kernelspec at:     {specfile}...")

    raw_spec = specfile.read_text(encoding="utf-8")

    print(raw_spec)

    spec = json.loads(raw_spec)

    print("""Checking python executable: {spec["argv"][0]}""")

    if spec["argv"][0].replace("\\", "/") != sys.executable.replace("\\", "/"):
        print(
            "The kernelspec seems to have the wrong prefix. \n"
            f"""    Specfile: {spec["argv"][0]}"""
            "\n"
            f"""    Expected: {sys.executable}"""
        )
        return 1

    return 0


def build_pytest_args() -> typing.List[str]:
    pytest_args = [
        "--color=yes",
        "--tb=long",
        "-vv",
        "--timeout=300",
        "--asyncio-mode=auto",
    ]

    if py_impl != "pypy":
        # coverage is very slow on pypy
        pytest_args += [
            "--cov=ipykernel",
            "--cov=branch",
            "--cov-report=term-missing:skip-covered",
            "--no-cov-on-fail",
        ]

    if is_win:
        test_skips.extend(
            [
                # test_pickleutil fails on windows, `pickleutil` deprecated anyway,
                "pickleutil",
            ]
        )

    if len(test_skips) == 1:
        # single-term parens work unexpectedly
        pytest_args += ["-k", f"not {test_skips}"]
    elif len(test_skips) > 1:
        pytest_args += ["-k", f"""not ({" or ".join(test_skips)})"""]

    return pytest_args


def run_pytest():
    if is_pypy and (is_aarch or is_ppc):
        print(f"Skipping pytest on {machine} for {py_impl}")
        return 0

    pytest_args = build_pytest_args()

    print("Final pytest args:", pytest_args, flush=True)

    # actually run the tests
    rc = int(pytest.main(pytest_args))

    if json.loads(os.environ.get("MIGRATING", "0").lower()):
        print("Ignoring pytest failure due to on-going migration...")
        return 0

    return rc


def main() -> int:
    return check_kernel() or run_pytest()


if __name__ == "__main__":
    sys.exit(main())
