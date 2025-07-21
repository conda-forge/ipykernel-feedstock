import os
from pathlib import Path
import sys
import json

UTF8 = {"encoding": "utf-8"}

prefix = Path(os.environ["PREFIX"])
kernel = "python{}".format(sys.version_info[0])
spec_path = prefix / "share/jupyter/kernels" / kernel / "kernel.json"
posix_exe = Path(sys.executable).as_posix()


def main() -> int:
    print("Rewriting kernelspec at:\n\t{}".format(spec_path))

    raw_spec = spec_path.read_text(**UTF8)

    print(raw_spec)

    spec = json.loads(raw_spec)

    print("Kernel python was:\n\t{}".format(spec["argv"][0]))

    if spec["argv"][0] == posix_exe:
        print("... OK")
    else:
        print("... rewriting kernel python with:\n\t{}".format(posix_exe))
        spec["argv"][0] = posix_exe
        raw_spec = json.dumps(spec, indent=2)
        print(raw_spec)
        spec_path.write_text(raw_spec, **UTF8)

    return 0


if __name__ == "__main__":
    sys.exit(main())
