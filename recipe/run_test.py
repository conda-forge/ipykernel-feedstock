import json
import os
import sys
import pytest


py_major = sys.version_info[0]
specfile = os.path.join(os.environ['PREFIX'], 'share', 'jupyter', 'kernels',
                        'python{}'.format(py_major), 'kernel.json')

print('Checking Kernelspec at:     ', specfile, '...\n')

with open(specfile, 'r') as fh:
    raw_spec = fh.read()

print(raw_spec)

spec = json.loads(raw_spec)

print('\nChecking python executable', spec['argv'][0], '...')

if spec['argv'][0].replace('\\', '/') != sys.executable.replace('\\', '/'):
    print('The kernelspec seems to have the wrong prefix. \n'
          'Specfile: {}\n'
          'Expected: {}'
           ''.format(spec['argv'][0], sys.executable))
    sys.exit(1)

if sys.platform.startswith("win") and sys.version_info >= (3, 8):
    import asyncio
    try:
        from asyncio import (
            WindowsProactorEventLoopPolicy,
            WindowsSelectorEventLoopPolicy,
        )
    except ImportError:
        pass
        # not affected
    else:
        if type(asyncio.get_event_loop_policy()) is WindowsProactorEventLoopPolicy:
            # WindowsProactorEventLoopPolicy is not compatible with tornado 6
            # fallback to the pre-3.8 default of Selector
            asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

sys.exit(pytest.main(["-m", "not flaky"]))
