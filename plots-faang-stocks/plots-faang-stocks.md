# This folder will contain the plots for the faang data.

## Author: Kyra Menai Hamilton

# Plots of the faang data

Each of the plots contained in this folder relate to a .csv file in the 'data-faang-stocks' folder.

They are automatically saved to this folder during the running of the code using:

```
output_plot_dir = r"plots-faang-stocks\"
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
```

# END