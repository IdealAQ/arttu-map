import pandas as pd
from pathlib import Path
import warnings



class DataHandler:
    """
    A class to handle data loading and processing.
    Takes a directory path as input and provides methods to load data files from that directory.
    Automatically removes data with missing latitude and longitude.
    Data can be filtered based on time intervals and location.
    """ 

    def __init__(self, config: dict):
        self.config = config
        self.data = None

    def load_data(self, data_directory: str, time_interval: tuple = None):
        """
        Load data from the specified directory.
        Optionally filter data based on a time interval and/or location.
        Saves the loaded data to self.data as a pandas DataFrame.
        
        :param time_interval: A tuple containing the start and end time in the format ("YYYY-MM-DD HH:MM:SS", "YYYY-MM-DD HH:MM:SS").
        """

        start_time = pd.to_datetime(time_interval[0]) if time_interval else None
        end_time = pd.to_datetime(time_interval[1]) if time_interval else None
        data_dir = Path(data_directory)

        # Iterate through each hour folder in the data directory and load any found CSV files
        dataframes = []
        for hour_folder in data_dir.iterdir():

        # Verify that the folder is a directory
            if not hour_folder.is_dir():
                continue

            # If a time interval is specified, filter the folders based on the time interval
            if start_time and end_time:
                try:
                     folder_start_time = pd.to_datetime(hour_folder.name, format="%Y-%m-%d_%H")
                except ValueError:
                    continue  # Skip folders that don't match the expected format when using time filtering
                
                # Skip folders outside the specified time interval
                folder_end_time = folder_start_time + pd.Timedelta(hours=1)
                if folder_end_time < start_time or folder_start_time > end_time:
                    continue
            
            # Load all CSV files in the hour folder
            for csv_file in hour_folder.glob("*.csv"):
                df = pd.read_csv(csv_file)
                dataframes.append(df)
        
        # Combine data frames, creating a new one if self.data is None, otherwise appending to the existing one
        combined_df = pd.concat(dataframes, ignore_index=True)
        if combined_df.empty: # If no data files were found in the specified directory and time interval, issue a warning and return
            warnings.warn(f"No data files found in the specified directory and time interval: {data_directory}, {time_interval}")
            return
        if self.data is None:
            self.data = combined_df
        else:
            self.data = pd.concat([self.data, combined_df], ignore_index=True)

        # If data config is provided, remove rows with missing latitude or longitude using the keys in the config
        if self.config is not None:
            self.remove_missing_lat_lon()
            
        
    def remove_missing_lat_lon(self):
        """
        Remove rows with missing latitude or longitude.
        """
        
        # Remove rows with missing latitude or longitude
        try:
            latitude_key = self.config["data"]["latitude_key"]
            longitude_key = self.config["data"]["longitude_key"]
            self.data.dropna(subset=[latitude_key, longitude_key], inplace=True)

        except KeyError as e: # If the keys are not found in the config
            raise KeyError(f"Missing key in configuration for latitude/longitude: {e}")
        except TypeError as e: # If self.data is not a DataFrame or is None
            raise TypeError(f"Data is not a DataFrame or is None: {e}")