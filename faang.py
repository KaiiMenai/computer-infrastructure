#!/usr/bin/env python3
# This program will contain the code to import and plot FAANG data.
# This is for the Computer Infrastructure course.

## Author: Kyra Menai Hamilton
## Date: 30/09/2025
## Version: 1.0

# First need to make sure the correct modules are installed.
# I decided to add all of these libraries because they are commonly used for data analysis and visualization and are allowed according to the requirements.
# See: https://github.com/ianmcloughlin/computer-infrastructure/blob/main/requirements.txt

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import datetime
import statsmodels as sm
import scipy as spy

# This code downloads the hourly data for the last 5 days for the 5 FAANG stocks (Facebook, Apple, Amazon, Netflix, Google) using the yfinance package.

def get_data():
    """Download FAANG hourly data for the last 5 days and return a DataFrame."""
    faang5_data = yf.download(tickers="AAPL AMZN META GOOG NFLX", period="5d", interval="1h") # adapted from https://stackoverflow.com/questions/74479906/how-to-get-aggregate-4hour-bars-historical-stock-data-using-yfinance-in-python
    print(faang5_data) # to check it works
    return faang5_data

# Directory handling and CSV saving have been moved into helper functions and are now performed inside `main()` below.
# This avoids running downloads/saves at import time and makes the module safe to import.
import os

# Now I want to create a function that opens the latest data file in the data-faang-stocks folder and plots the closing prices of each stock over time.
# I will use the date as the title for the plot. https://www.kaggle.com/code/leeyongbin/faang-stock-data-visualization

def plot_data():
    # Use data directory where CSVs are saved
    data_dir = ensure_dir("data-faang-stocks/")
    files = os.listdir(data_dir)
    # Filter out only CSV files
    csv_files = [f for f in files if f.lower().endswith('.csv')]
    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return

    # Sort the files by modification time in descending order and pick latest
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
    latest_file = csv_files[0]
    latest_file_path = os.path.join(data_dir, latest_file)
    print(f"Using latest CSV: {latest_file}")

    tickers = ["AAPL", "AMZN", "META", "GOOG", "NFLX"]

    # Try reading the CSV that was saved with a 3-line header (Price / Ticker / Datetime) https://sparkbyexamples.com/pandas/pandas-multiindex-dataframe-examples/#:~:text=Pandas%20MultiIndex%20to%20Columns,to%20DataFrame%20starting%20from%20zero.
    try:
        # The CSV has a multi-row header: first row contains Price/Close/High/..., second the tickers. - https://towardsdatascience.com/working-with-multi-index-pandas-dataframes-f64d2e2c3e02/, https://pandas.pydata.org/docs/user_guide/advanced.html
        # The third row in the file contains the literal 'Datetime' in the first column which will be skipped.
        data = pd.read_csv(latest_file_path, header=[0, 1], skiprows=[2], index_col=0, parse_dates=True)
    except Exception as e:
        print("Warning: failed to read CSV with MultiIndex header, trying fallback. Error:", e) # This will help find error cause.
        # Try to read normally and attempt to promote the first data row to column level 1 if it contains tickers - not entirely necessary but noted just incase
        data = pd.read_csv(latest_file_path, index_col=0, parse_dates=True)
        # If the first row contains ticker symbols, promote it to second-level header -  https://www.datacamp.com/tutorial/pandas-read-csv
        try:
            first_row = data.iloc[0]
            # if the first row contains one of the expected tickers, use it as second header 
            if any(str(x) in tickers for x in first_row.values):
                new_cols = pd.MultiIndex.from_arrays([data.columns, first_row.values])
                data = data[1:]
                data.columns = new_cols
                data.index = pd.to_datetime(data.index)
                print("Promoted first data row to MultiIndex column level")
        except Exception:
            # If anything goes wrong, continue available columns will be detected with the following
            pass

    # Make a dataframe of closing prices called close_df. - https://realpython.com/pandas-dataframe/
    close_df = None
    if isinstance(data.columns, pd.MultiIndex): # Using the if/else will help avoid errors if the CSV doesn't have multi-level columns. (but I know it does after a manual check).
        # Normally, it will be: top-level contains 'Close', second-level contains tickers
        if 'Close' in data.columns.get_level_values(0):
            close_df = data['Close']
        else:
            # Try to find a top-level name that includes 'Close'
            top_levels = list(dict.fromkeys(data.columns.get_level_values(0)))
            print("Top-level column names found:", top_levels)
            for name in top_levels:
                if 'Close' in str(name):
                    close_df = data[name]
                    break
    else:
        # Single-level columns: try to find columns that mention 'Close'
        close_cols = [c for c in data.columns if 'Close' in str(c)]
        if close_cols:
            close_df = data[close_cols]

    if close_df is None:
        print("Could not find 'Close' columns. Available columns (first 30):")
        print(list(data.columns)[:30])
        raise KeyError("Close columns not found in CSV - file format not recognised")

    # Plot the closing prices of each stock over time (only when available) - this will be done per hourly data over the 5 days of the data (included in the .csv).
    fig, ax = plt.subplots(figsize=(14, 7))
    for ticker in tickers:
        if ticker in close_df.columns:
            # Make sure values are numeric
            series = pd.to_numeric(close_df[ticker], errors='coerce')
            ax.plot(series.index, series.values, label=ticker)
        else:
            print(f"Ticker {ticker} not found in Close data; available: {list(close_df.columns)}")

    ax.set_title(f"FAANG Stock Closing Prices - {latest_file.split('.')[0]}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price (USD)")
    ax.legend()
    ax.grid()
    fig.tight_layout()
    # Show the plot interactively (optional) and return the Figure so it can be saved
    plt.show()
    return fig
    
def ensure_dir(path):
    """Create directory if missing and return absolute path."""
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.abspath(path)


def save_csv(data, output_dir):
    absolute_output_dir = ensure_dir(output_dir)
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join(absolute_output_dir, f"{current_time}.csv")
    data.to_csv(file_path, date_format='%Y-%m-%d %H:%M:%S')
    print(f"File saved at: {file_path}")
    print(f"Absolute path to output directory: {absolute_output_dir}")
    print("Files in directory:", os.listdir(output_dir))
    return file_path, absolute_output_dir


def save_plot(fig, output_plot_dir):
    absolute_output_plot_dir = ensure_dir(output_plot_dir)
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_plot_path = os.path.join(absolute_output_plot_dir, f"{current_time}.png")
    if fig is not None:
        try:
            fig.savefig(file_plot_path, bbox_inches='tight', dpi=150)
        except Exception as e:
            print(f"Failed to save figure: {e}")
    else:
        print("No figure returned from plot_data(); nothing to save.")
    print(f"File saved at: {file_plot_path}")
    print(f"Absolute path to output directory: {absolute_output_plot_dir}")
    print("Files in directory:", os.listdir(output_plot_dir))
    return file_plot_path, absolute_output_plot_dir


def main():
    # download and save data
    faang5_data = get_data()
    print("Data types of each column:" , faang5_data.dtypes)
    save_csv(faang5_data, "data-faang-stocks/")

    # make plot and save
    fig = plot_data()
    save_plot(fig, "plots-faang-stocks/")


if __name__ == "__main__":
    main()

# Next get this to be automated and run every Saturday.
# need to specify this in the README file, and create a requirements.txt file for the necessary packages, as well as allowing it to be run in a virtual environment.
# will also need to add permissions to run the script automatically every Saturday.

# 29/11/25 - updated the code to run through a virtual environment.
# working in codespaces I had git commit issues it gave a git user.name error 403 - so to check the username and display name were the same to fix issue.

# Git commission issue fixed by setting the git config user.name and user.email to match the GitHub account used for codespaces.

# Automation problems detected.
# Automation problems fixed - copied and adapted the code by Ian - realised I could have done the same with my own that I had originally written as the problem was actually in the .py and save location, not the workflow itself.

# END