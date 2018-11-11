import json
import os
import sys


py_major = sys.version_info[0]
specfile = os.path.join(os.environ['PREFIX'], 'share', 'jupyter', 'kernels',
                        'python{}'.format(py_major), 'kernel.json')

print('Checking Kernelspec at', specfile, "...")

with open(specfile, 'r') as fh:
    spec = json.load(fh)

print("Checking python executable", spec['argv'][0], "...")

if spec['argv'][0].replace('\\', '/') != sys.executable.replace('\\', '/'):
    raise ValueError('The specfile seems to have the wrong prefix. \n'
                     'Specfile: {}; Expected: {};'
                     ''.format(spec['argv'][0], sys.executable))

if os.name == "nt":
    # as of ipykernel 5.1.0, a number of async tests fail on windows, and
    # `pytest --pyargs` doesn't work properly with `-k` or `--ignore`
    from ipykernel.tests import test_async
    print("Windows: Removing", test_async.__file__)
    os.unlink(test_async.__file__)
