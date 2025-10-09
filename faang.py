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

# Now to save it as a .csv file in a folder called data-faang-stocks in the root repository with the correct naming format YYYYMMDD-HHmmss.csv. and make sure I don't lose the date and time index.
# Save the data to a CSV file
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_path = os.path.join(absolute_output_dir, f"{current_time}.csv")
faang5_data.to_csv(file_path, date_format='%Y-%m-%d %H:%M:%S') # adapted from https://stackoverflow.com/questions/30298144/datetime-format-change-when-save-to-csv-file-python

# Verify the file was saved
print(f"File saved at: {file_path}")
print(f"Absolute path to output directory: {absolute_output_dir}")
print("Files in directory:", os.listdir(output_dir))

# Need to make sure that the file is saved in the correct type - integer, float etc.
data_types = faang5_data.dtypes
print("Data types of each column:" , data_types) # with floats and ints it will make it harder to plot the data.


# Now I want to create a function that opens the latest data file in the data-faang-stocks folder and plots the closing prices of each stock over time.
# I will use the date as the title for the plot. https://www.kaggle.com/code/leeyongbin/faang-stock-data-visualization

# END