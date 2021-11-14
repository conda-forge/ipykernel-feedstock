import json
import os
import platform
import sys
import pkgutil
import pytest

py_major = sys.version_info[0]
py_impl = platform.python_implementation().lower()

print("Python implementation:", py_impl)
specfile = os.path.join(
    os.environ["PREFIX"],
    "share",
    "jupyter",
    "kernels",
    "python{}".format(py_major),
    "kernel.json",
)

print("Checking Kernelspec at:     ", specfile, "...\n")

with open(specfile, "r") as fh:
    raw_spec = fh.read()

print(raw_spec)

spec = json.loads(raw_spec)

print("\nChecking python executable", spec["argv"][0], "...")

if spec["argv"][0].replace("\\", "/") != sys.executable.replace("\\", "/"):
    print(
        "The kernelspec seems to have the wrong prefix. \n"
        "Specfile: {}\n"
        "Expected: {}"
        "".format(spec["argv"][0], sys.executable)
    )
    sys.exit(1)

loader = pkgutil.get_loader("ipykernel.tests")
pytest_args = [os.path.dirname(loader.path), "-vv", "--timeout", "300"]

# coverage options
pytest_args += [
    "--cov",
    "ipykernel",
    "--cov-report",
    "term-missing:skip-covered",
    "--no-cov-on-fail",
]

# TODO: investigate upstream interrupt regression in 6.5.0
skips = ["flaky", "interrupt"]

if len(skips) == 1:
    pytest_args += ["-k", "not {}".format(*skips)]
else:
    pytest_args += ["-k", "not ({})".format(" or ".join(skips))]

print("Final pytest args:", pytest_args)

# actually run the tests
rc = pytest.main(pytest_args)

if json.loads(os.environ.get("MIGRATING", "0").lower()):
    print("Ignoring pytest failure due to on-going migration...")
    sys.exit(0)

sys.exit(rc)
