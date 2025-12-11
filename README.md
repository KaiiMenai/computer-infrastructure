# Computer Infrastructure

This folder will contain work for the Computer Interface module. It will cover several disciplines throughout the duration of the project.

## Overview

This repository forms the basis of work and analysis carried out for the Computer Infrastructure Module.

The content will be split into 4 segments:

1. Retrieving the data.
2. Cleaning and the data and plotting the data.
3. FIND IT
4. Automation of using the workflows.

## Steps

Prior to any data analysis, it was important to get the correct Modules downloaded Nd installed into the workspace. The full list is found in `requiremets.txt`.

Should an error message appear, use the ```pip install``` command in the terminal, to ensure that the required packages are installed.

Next, its time to get the data. For this two methods can be used. The first involves ```url ='url'``` where data is sourced directly from the url, the second involves saving the data as a .csv.
As saving the data in csv form directly to a file using python is part of the requirements for this task, I shall discuss this was done from the url and saved as a csv in the `data-faang-data` folder. The data and time of url access and saving was used as the file name. this was also used for the plot later in order for accurate referencing between data file and plot.

## Jupyter

## Cross-platform instructions (Windows / macOS / Linux)

This project includes [faang.py](D:\Data_Analytics\Modules\CI\computer-infrastructure\faang.py), a Python script that downloads and plots [FAANG stock data] (REF). Use the instructions below to run it on Windows, macOS and Linux.
The current [faang.py](D:\Data_Analytics\Modules\CI\computer-infrastructure\faang.py) was written in VS Code on desktop.The file includes a portable shebang (for example `#!/usr/bin/env python3.12`). Some modifications will be necessary for smooth implementation elsewhere.

### Requirements

- Python 3.12 (recommended) or any Python 3.x compatible with the packages in `requirements.txt`.
- Recommended virtual environment: `venv`, `conda`, or `pipenv`.
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

### Jupyter / Notebook usage

## Files and outputs

- CSV output directory: `data-faang-stocks/`
- Plots directory: `plots-faang-stocks/`
- Plot filename pattern: `YYYYMMDD-HHMMSS.png` (script uses current timestamp)

## Troubleshooting hints

## References

- pandas `read_csv` — using `header`, `skiprows`, `index_col`, `parse_dates`:
	https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
- pandas MultiIndex columns and selection:
	https://pandas.pydata.org/docs/user_guide/advanced.html#advanced-multiindex
- pandas I/O guide (CSV writing/reading):
	https://pandas.pydata.org/docs/user_guide/io.html
- matplotlib `plot` and `savefig`:
	https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
	https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html
- yfinance (package and repo):
	https://github.com/ranaroussi/yfinance
- Virtual environments (`venv`) documentation:
	https://docs.python.org/3/library/venv.html
- pip (package installer) docs:
	https://pip.pypa.io/en/stable/
- conda quickstart:
	https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html
- Python launcher for Windows (py):
	https://docs.python.org/3/using/windows.html#python-launcher-for-windows
- Shebang explanation and best practices:
	https://en.wikipedia.org/wiki/Shebang_(Unix)
- Jupyter and nbconvert (running/converting notebooks to scripts):
	https://jupyter.org/
	https://nbconvert.readthedocs.io/
- Scheduling and automation:
	- Windows Task Scheduler overview: https://learn.microsoft.com/windows/win32/taskschd/task-scheduler-start-page
	- Cron (Linux scheduling): https://opensource.com/article/17/11/how-use-cron-linux
	- systemd timer units: https://www.freedesktop.org/software/systemd/man/systemd.timer.html
- Troubleshooting related Q&As:
	- Pandas date parse warning: https://stackoverflow.com/questions/48050194/pandas-read-csv-warning-could-not-infer-format-so-each-element-will-be-parsed-in
	- Reading CSV with MultiIndex header: https://stackoverflow.com/questions/49023958/how-to-read-csv-with-multiindex-columns-using-pandas
	- Handling MultiIndex columns and selection: https://stackoverflow.com/questions/32385343/handling-multiindex-columns-in-pandas

---

# END