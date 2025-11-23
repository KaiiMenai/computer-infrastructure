#!/usr/bin/env python3.12
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

faang5_data = yf.download(tickers="AAPL AMZN META GOOG NFLX", period="5d", interval="1h") # adapted from https://stackoverflow.com/questions/74479906/how-to-get-aggregate-4hour-bars-historical-stock-data-using-yfinance-in-python

def get_data(faang5_data): 
    print(faang5_data) # to check it works
    return faang5_data 

# Now need to call the function to get the data
get_data(faang5_data)

# I kept getting an error that the folder didn't exist so I created it manually in the root repository.
# So now I need to check that the directory exists before trying to save the file.
import os
output_dir = r"D:\Data_Analytics\Modules\CI\computer-infrastructure\data-faang-stocks"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
    # Get the absolute path of the output directory
absolute_output_dir = os.path.abspath(output_dir)

# Need to make sure that the file is saved in the correct type - integer, float etc.
data_types = faang5_data.dtypes
print("Data types of each column:" , data_types) # with floats and ints it will make it harder to plot the data.

# Now to save it as a .csv file in a folder called data-faang-stocks in the root repository with the correct naming format YYYYMMDD-HHmmss.csv. and make sure I don't lose the date and time index.
# Save the data to a CSV file
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_path = os.path.join(absolute_output_dir, f"{current_time}.csv")
faang5_data.to_csv(file_path, date_format='%Y-%m-%d %H:%M:%S') # adapted from https://stackoverflow.com/questions/30298144/datetime-format-change-when-save-to-csv-file-python

# Verify the file was saved
print(f"File saved at: {file_path}")
print(f"Absolute path to output directory: {absolute_output_dir}")
print("Files in directory:", os.listdir(output_dir))

# Now I want to create a function that opens the latest data file in the data-faang-stocks folder and plots the closing prices of each stock over time.
# I will use the date as the title for the plot. https://www.kaggle.com/code/leeyongbin/faang-stock-data-visualization

def plot_data():
    # Get the list of files in the directory
    files = os.listdir(absolute_output_dir)
    # Filter out only CSV files
    csv_files = [f for f in files if f.lower().endswith('.csv')]
    if not csv_files:
        print(f"No CSV files found in {absolute_output_dir}")
        return

    # Sort the files by modification time in descending order and pick latest
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(absolute_output_dir, x)), reverse=True)
    latest_file = csv_files[0]
    latest_file_path = os.path.join(absolute_output_dir, latest_file)
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
    # Show the plot interactively (optional) and return the Figure so caller can save it
    plt.show()
    return fig
    
# Now to call the function to plot the data and capture the Figure for saving
fig = plot_data() # easier to access for saving.

# Now that I know it works, I will add comments and references to the code in jupyter to explain what each part does.

# Now to save the plot as a .png file in a folder called plots-faang-stocks in the root repository with the correct naming format YYYYMMDD-HHmmss.csv. and make sure I don't lose the date and time index.

output_plot_dir = r"D:\Data_Analytics\Modules\CI\computer-infrastructure\plots-faang-stocks"
if not os.path.exists(output_plot_dir):
    os.makedirs(output_plot_dir)
    # Get the absolute path of the output directory
absolute_output_plot_dir = os.path.abspath(output_plot_dir)

# Save the plot to a PNG file using the returned Figure - modified code from what was being used for csv saving
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_plot_path = os.path.join(absolute_output_plot_dir, f"{current_time}.png")
if fig is not None:
    try:
        fig.savefig(file_plot_path, bbox_inches='tight', dpi=150)
    except Exception as e:
        print(f"Failed to save figure: {e}")
else:
    print("No figure returned from plot_data(); nothing to save.")

# Verify the file was saved
print(f"File saved at: {file_plot_path}")
print(f"Absolute path to output directory: {absolute_output_plot_dir}")
print("Files in directory:", os.listdir(output_plot_dir))

# Next get this to be automated and run every Saturday.
# need to specify this in the README file, and create a requirements.txt file for the necessary packages, as well as allowing it to be run in a virtual environment.
# will also need to add permissions to run the script automatically every Saturday.



# END