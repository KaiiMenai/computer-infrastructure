# This folder will contain the data for the faang stocks.

## Author: Kyra Menai Hamilton

# CSV files of the faang data

Data for the faang extracted data will be in this folder

The data was saved to this folder automatically, here are some code excerpts:

```python
# Source the data
def get_data():
    """Download FAANG hourly data for the last 5 days and return a DataFrame."""
    faang5_data = yf.download(tickers="AAPL AMZN META GOOG NFLX", period="5d", interval="1h") # adapted from https://stackoverflow.com/questions/74479906/how-to-get-aggregate-4hour-bars-historical-stock-data-using-yfinance-in-python
    print(faang5_data) # to check it works
    return faang5_data

# Save the data to a CSV file

    # download and save data
    faang5_data = get_data()
    print("Data types of each column:" , faang5_data.dtypes)
    save_csv(faang5_data, "data-faang-stocks/")

# Naming save file
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_path = os.path.join(absolute_output_dir, f"{current_time}.csv")
faang5_data.to_csv(file_path, date_format='%Y-%m-%d %H:%M:%S') # adapted from https://stackoverflow.com/questions/30298144/datetime-format-change-when-save-to-csv-file-python

# Verify the file was saved
print(f"File saved at: {file_path}")
print(f"Absolute path to output directory: {absolute_output_dir}")
print("Files in directory:", os.listdir(output_dir))
```

# END