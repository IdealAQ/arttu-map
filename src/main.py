from data_handler import DataHandler
import yaml



# Define the time interval from which to extract the data
time_interval = ("2026-06-30 00:00:00", "2026-07-03 23:59:59")

# Load the data configuration from the YAML file
with open("data_configuration.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Initialize the DataHandler with the path to the testing data directory
data_handler = DataHandler(config=config)

data_directory = "testing_data"  # Path to the directory containing the data files

# Load the data from the specified directory and time interval
data_handler.load_data(data_directory=data_directory, time_interval=time_interval)

# Save data
data_handler.save_data(output_file_path="testing_data/processed_test_data.parquet")