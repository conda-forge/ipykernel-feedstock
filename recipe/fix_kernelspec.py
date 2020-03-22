import os
from pathlib import Path
import sys
import json

prefix = Path(os.environ["PREFIX"])
kernel = "python{}".format(sys.version_info[0])
spec_path = prefix / "share" / "jupyter" / "kernels" / kernel / "kernel.json"
posix_exe = Path(sys.executable).as_posix()

print("Rewriting kernelspec at:\n\t{}".format(spec_path))

spec = json.loads(spec.spec_path())

print("Kernel python was:\n\t{}".format(spec["argv"][0]))

spec["argv"][0] = posix_exe

print("Rewriting kernel python with:\n\t{}".format(posix_exe))

spec_path.write_text(json.dumps(spec, indent=2))
