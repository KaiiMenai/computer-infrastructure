# Data

Data for the faang extracted data will be in this folder

The data was saved to this folder automatically using the code:

```
# Save the data to a CSV file
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_path = os.path.join(absolute_output_dir, f"{current_time}.csv")
faang5_data.to_csv(file_path, date_format='%Y-%m-%d %H:%M:%S') # adapted from https://stackoverflow.com/questions/30298144/datetime-format-change-when-save-to-csv-file-python

# Verify the file was saved
print(f"File saved at: {file_path}")
print(f"Absolute path to output directory: {absolute_output_dir}")
print("Files in directory:", os.listdir(output_dir))
```

# END