@echo off

:: Install kernelspec at post-link because conda doesn't substitute Windows paths correctly in JSON files
:: One error conda makes is that it doesn't remove the `bin` folder from the python path.
:: Second, it doesn't add the `.exe` extention.
:: See discussion in https://github.com/conda-forge/ipykernel-feedstock/issues/37
"%PREFIX%"\Python.exe -m ipykernel install --sys-prefix > NUL 2>&1 && if errorlevel 1 exit 1
