# computer-infrastructure

This folder will contain work for the CI module

## Jupyter

## Cross-platform instructions

This project includes [faang.py](D:\Data_Analytics\Modules\CI\computer-infrastructure\faang.py), a Python script that downloads and plots [FAANG stock data] (REF). Use the instructions below to run it on Windows, macOS and Linux.
The current [faang.py](D:\Data_Analytics\Modules\CI\computer-infrastructure\faang.py) was written in VS Code on desktop. Some modifications will be necessary for smooth implementation elsewhere.

### Requirements

- Python 3.12 (recommended) or any Python 3.x compatible with the packages in `requirements.txt`.
- Recommended virtual environment (venv, pipenv, or conda).
- Required Python packages: `pandas, matplotlib, seaborn, yfinance, numpy, statsmodels, scipy` (install via pip or conda).

An Example using pip:

```
# Powershell (Windows)
pythosn -m vsnv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Alternatively:

```
# macOS / Linux
python3 -m venv .venv
source .vemv/bin/active
pip install -r requirements.txt
```

Once installed run the program.

#### Running on Windows

Windows ignores the shebang line. Use the Python launcher (py) or call the full python.exe path.

- Run with the Python launcher (selects installed Python version):

```
# Use the py launcher to run with Python 3.12 specifically - for minimal issues.
py -3.12 d:\Data_Analytics\Modules\CI\computer-infrastructure\faang.py
```

- Or run via the active venv/python:

```
# From project root after activating venv
python d:\Data_Analytics\Modules\CI\computer-infrastructure\faang.py
```

- If you need a scheduled run, create a Task in Windows Task Scheduler that runs the above py or python command.

#### Running on macOS / Linux


Currently testing to make sure that everything is working as expected.

Looking at setting up automatic workflows.

- need to add workflow template.
- modify to create a condition where something like "if Saturday = X".
- test workflow using alternate days initially then change to a Saturday.

# END