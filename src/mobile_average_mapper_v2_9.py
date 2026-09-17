import warnings
import json
import matplotlib as mpl
import datetime as dt
import pandas as pd
import numpy as np
import math
import folium
import folium.plugins
from tqdm import tqdm
from pyproj import Transformer
from folium.plugins import HeatMap
import json
import uuid

class MobileMeasurementMapper():
    """
    A class to map and analyze mobile measurements from JSON files. 
    """
    
    # Define keys for the measured variables
    KEY_CH4 = "airsence_ch4_ppm" #"airsence_ch4"
    KEY_CO = "airsence_co_ppb" #"airsence_co"
    KEY_CO2 = "airsence_co2_ppm" #"airsence_co2"
    KEY_HUMIDITY = "airsence_humamb_x" #"airsence_hum_amb"
    KEY_H2S = "airsence_h2s_ppb" #"airsence_h2s"
    
    KEY_LATITUDE = "location_lat" #"location_latitude"
    #KEY_LATITUDE = "gps_lat"
    
    KEY_LIGHT = "airsence_lux_xx" #"airsence_lux"
    
    KEY_LONGITUDE = "location_long" #"location_longitude"
    #KEY_LONGITUDE = "gps_lon"
    
    KEY_NH3 = "airsence_nh3_ppm" #"airsence_nh3"
    KEY_NO = "airsence_no_ppb" #"airsence_no"
    KEY_NO2 = "airsence_no2_ppb" #"airsence_no2"
    KEY_NOISE_AIRSENCE = "airsence_noiseleq_db" #"airsence_noise_leq"
    KEY_O3 = "airsence_o3_ppb" #"airsence_o3"
    
    KEY_PM1_ALPOPC = "alphopc_pm1p0_ugm3"
    KEY_PM2_5_ALPOPC = "alphopc_pm2p5_ugm3"
    #KEY_PM4_ALPOPC = "alphopc_pm4p0_ugm3"
    KEY_PM10_ALPOPC = "alphopc_pm10p0_ugm3"
    
    KEY_PRESSURE_AIRSENCE = "airsence_pressureamb_x"
    KEY_SO2 = "airsence_so2_ppb"
    KEY_TEMPERATURE_AIRSENCE = "airsence_tempamb_x"
    
    KEY_WINDSPEED = "airsence_windspeed_xx"
    
    KEY_TIME = "timestamp"
    #KEY_TIME = "time"
    
    KEY_NUMBER = "naneos_number"
    KEY_DIAMETER = "naneos_diameter"
    KEY_LDSA = "naneos_ldsa"
    KEY_SURFACE_AREA = "naneos_total_surface_area"
    KEY_GEOMETRIC_STANDARD_DEVIATION = "naneos_geom_std_dev"
    KEY_DNDLOGD1 = "naneos_dNdlogD1"
    KEY_DNDLOGD2 = "naneos_dNdlogD2"
    KEY_DNDLOGD3 = "naneos_dNdlogD3"
    KEY_DNDLOGD4 = "naneos_dNdlogD4"
    KEY_DNDLOGD5 = "naneos_dNdlogD5"
    KEY_DNDLOGD6 = "naneos_dNdlogD6"
    KEY_DNDLOGD7 = "naneos_dNdlogD7"
    KEY_DNDLOGD8 = "naneos_dNdlogD8"
    KEY_VOC = "airsence_voc_ppm"
    
    KEY_PNC_PPLUS = "pplus_pnc_ptcm3"
    KEY_PM2_5_PPLUS = "pplus_pm2p5_ugm3"
    KEY_PM10_PPLUS = "pplus_pm10_ugm3"
    KEY_DNDLOGDP300T350_PPLUS = "pplus_dNdlogdP300to350nm_ptcm3"
    KEY_DNDLOGDP350T400_PPLUS = "pplus_dNdlogdP350to400nm_ptcm3"
    KEY_DNDLOGDP400T450_PPLUS = "pplus_dNdlogdP400to450nm_ptcm3"
    KEY_DNDLOGDP450T500_PPLUS = "pplus_dNdlogdP450to500nm_ptcm3"
    KEY_DNDLOGDP500T550_PPLUS = "pplus_dNdlogdP500to550nm_ptcm3"
    KEY_DNDLOGDP550T600_PPLUS = "pplus_dNdlogdP550to600nm_ptcm3"
    KEY_DNDLOGDP600T650_PPLUS = "pplus_dNdlogdP600to650nm_ptcm3"
    KEY_DNDLOGDP650T700_PPLUS = "pplus_dNdlogdP650to700nm_ptcm3"
    KEY_DNDLOGDP700T800_PPLUS = "pplus_dNdlogdP700to800nm_ptcm3"
    KEY_DNDLOGDP800T900_PPLUS = "pplus_dNdlogdP800to900nm_ptcm3"
    KEY_DNDLOGDP900T1000_PPLUS = "pplus_dNdlogdP900to1000nm_ptcm3"
    KEY_DNDLOGDP1000T1250_PPLUS = "pplus_dNdlogdP1000to1250nm_ptcm3"
    KEY_DNDLOGDP1250T1500_PPLUS = "pplus_dNdlogdP1250to1500nm_ptcm3"
    KEY_DNDLOGDP1500T2000_PPLUS = "pplus_dNdlogdP1500to2000nm_ptcm3"
    KEY_DNDLOGDP2000T2500_PPLUS = "pplus_dNdlogdP2000to2500nm_ptcm3"
    KEY_DNDLOGDP2500T3000_PPLUS = "pplus_dNdlogdP2500to3000nm_ptcm3"
    KEY_DNDLOGDP3000T3500_PPLUS = "pplus_dNdlogdP3000to3500nm_ptcm3"
    KEY_DNDLOGDP3500T4000_PPLUS = "pplus_dNdlogdP3500to4000nm_ptcm3"
    KEY_DNDLOGDP4000T4500_PPLUS = "pplus_dNdlogdP4000to4500nm_ptcm3"
    KEY_DNDLOGDP4500T5000_PPLUS = "pplus_dNdlogdP4500to5000nm_ptcm3"
    KEY_DNDLOGD5000T5500_PPLUS = "pplus_dNdlogdP5000to5500nm_ptcm3"
    KEY_DNDLOGDP5500T6000_PPLUS = "pplus_dNdlogdP5500to6000nm_ptcm3"
    KEY_DNDLOGDP6000T6500_PPLUS = "pplus_dNdlogdP6000to6500nm_ptcm3"
    KEY_DNDLOGDP6500T7000_PPLUS = "pplus_dNdlogdP6500to7000nm_ptcm3"
    KEY_DNDLOGDP7000T7500_PPLUS = "pplus_dNdlogdP7000to7500nm_ptcm3"
    KEY_DNDLOGDP7500T8000_PPLUS = "pplus_dNdlogdP7500to8000nm_ptcm3"
    KEY_DNDLOGDP8000T8500_PPLUS = "pplus_dNdlogdP8000to8500nm_ptcm3"
    KEY_DNDLOGDP8500T9250_PPLUS = "pplus_dNdlogdP8500to9250nm_ptcm3"
    KEY_DNDLOGDP9250T10000_PPLUS = "pplus_dNdlogdP9250to10000nm_ptcm3"
    KEY_DNDLOGDP10000T25000_PPLUS = "pplus_dNdlogdP10000to25000nm_ptcm3"
    
    KEY_TEMPERATURE_HDC3022 = "hdc3022_temp_c"
    KEY_HUMIDITY_HDC3022 = "hdc3022_rh_pct"
    
    KEY_NOISELEQ_NSRTMK4 = "nsrtmk4_noiseleq_db"
    
    KEY_ACCELERATION_X = "imu_acceleration_x"
    KEY_ACCELERATION_Y = "imu_acceleration_y"
    KEY_ACCELERATION_Z = "imu_acceleration_z"
    KEY_ACCELERATION_RMS = "imu_rms_acceleration"
    
    KEY_BACKGROUND_TEMPERATURE = "background_temp_c"
    KEY_TEMPERATURE_DIFFERENCE = "temp_diff_c"
    
    KEY_MRT = "mrtmax31865_temp_c"
    KEY_MRT_DIFFERENCE = "MRT_airtemp_diff_c"
    KEY_MRT_BACKGROUND_DIFFERENCE = "MRT_airtemp_diff_background_c"
    
    KEY_PHIDGET_TEMPERATURE = "phidget_temp_c"
    
    KEY_PET = "pet_c"
    KEY_UTCI = "utci_c"
    
    KEY_POTHOLE = "scanwai_pothole"
    KEY_POTHOLE_PERMALINK = "scanwai_permalink"
    
    KEY_OBSERVATION_TYPE = "obs_type"
    
    

    def __init__(self, 
                 json_files=None, 
                 output_json_filename:str=None,
                 output_map_filename:str=None,
                 starting_zoom:int=13,
                 point_size:int=1,
                 units:dict=None,
                 default_plotting:str="linear",
                 plotting:dict=None, 
                 limits:dict=None, 
                 tagged_only:dict=None,
                 bin_size_m:float=50,
                 histogram:bool=False,
                 display_counts:bool=False,
                 start_time:str=None, 
                 end_time:str=None, 
                 min_lat:float=None, 
                 max_lat:float=None, 
                 min_lon:float=None, 
                 max_lon:float=None):
        """
        Initializes the MobileMeasurementMapper with JSON files, units, and limits.
        """
        
        #self.to_utm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        #self.to_wgs = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
        #self.to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32635", always_xy=True)
        #self.to_wgs = Transformer.from_crs("EPSG:32635", "EPSG:4326", always_xy=True)
        self.to_utm = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)
        self.to_wgs = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True)
        self.utci_supported_keys = [self.KEY_UTCI, self.KEY_PET, self.KEY_TEMPERATURE_AIRSENCE, self.KEY_TEMPERATURE_HDC3022, self.KEY_MRT, self.KEY_BACKGROUND_TEMPERATURE]
        self.utci_values = {
            "Extreme Cold Stress": [-40, "#08306B"],
            "Very Strong Cold Stress": [-27, "#2171B5"],
            "Strong Cold Stress": [-13, "#6BAED6"],
            "Moderate Cold Stress": [0, "#9ECAE1"],
            "Slight Cold Stress": [9, "#B2E2E2"],
            "No Thermal Stress": [26, "#4DAF4A"],
            "Moderate Heat Stress": [32, "#FFD92F"],
            "Strong heat stress": [38, "#FDAE61"],
            "Very Strong Heat Stress": [46, "#D73027"],
            "Extreme Heat Stress": [999999999999, "#67000D"]
        }
        self.utci = pd.DataFrame(self.utci_values).T
        self.naneos_number_discrete_values = {
            "Low": [10000, "#4DAF4A"],
            "Medium": [20000, "#FFD92F"],
            "High": [50000, "#FF0000"],
            "Very High": [9999999999, "#BF40BF"]
        }
        self.naneos_number_discrete = pd.DataFrame(self.naneos_number_discrete_values).T
        self.pm2_5_discrete_values = {
            "Low": [15, "#4DAF4A"],
            "Medium": [35, "#FFD92F"],
            "High": [55, "#FF0000"],
            "Very High": [9999999999, "#BF40BF"] 
        }
        self.pm2_5_discrete = pd.DataFrame(self.pm2_5_discrete_values).T
        self.pm10_discrete_values = {
            "Low": [45, "#4DAF4A"],
            "Medium": [90, "#FFD92F"],
            "High": [195, "#FF0000"],
            "Very High": [9999999999, "#BF40BF"]
        }
        self.pm10_discrete = pd.DataFrame(self.pm10_discrete_values).T
        self.rms_acceleration_discrete_values = {
            "Low": [0.30, "#4DAF4A"],
            "High": [9999999999, "#FF0000"],
        }
        self.rms_acceleration_discrete = pd.DataFrame(self.rms_acceleration_discrete_values).T
        self.default_plotting = default_plotting # Set the default plotting type
        self.bin_size_m = bin_size_m # Set the bin size for binned data
        self.histogram = histogram # Set the histogram flag
        self.data = None # Initialize data as None
        self.map = None # Initialize map as None
        self.layers = {} # Initialize layers as an empty dictionary
        self.starting_zoom = starting_zoom # Set the starting zoom level for the map
        self.point_size = point_size # Set the point size for the markers on the map
        self.display_counts = display_counts # Set the flag to display counts
        self.min_max = {} # Initialize min_max as an empty dictionary
        self.legends = {} # Initialize legends as an empty dictionary
        self.units = { #Set default units for each key
            self.KEY_CH4: "ppm",
            self.KEY_CO: "ppb",
            self.KEY_CO2: "ppm",
            self.KEY_HUMIDITY: "%",
            self.KEY_H2S: "ppm",
            self.KEY_LATITUDE: "°",
            self.KEY_LIGHT: "lux",
            self.KEY_LONGITUDE: "°",
            self.KEY_NO: "ppb",
            self.KEY_NO2: "ppb",
            self.KEY_NOISE_AIRSENCE: "dBA",
            self.KEY_O3: "ppb",
            self.KEY_PM1_ALPOPC: "μg/m³",
            self.KEY_PM2_5_ALPOPC: "μg/m³",
            #self.KEY_PM4_ALPOPC: "μg/m³",
            self.KEY_PM10_ALPOPC: "μg/m³",
            self.KEY_PRESSURE_AIRSENCE: "hPa",
            self.KEY_SO2: "ppb",
            self.KEY_TEMPERATURE_AIRSENCE: "°C",
            self.KEY_NUMBER: "",
            self.KEY_DIAMETER: "",
            self.KEY_LDSA: "",
            self.KEY_SURFACE_AREA: "",
            self.KEY_GEOMETRIC_STANDARD_DEVIATION: "",
            self.KEY_DNDLOGD1: "",
            self.KEY_DNDLOGD2: "",
            self.KEY_DNDLOGD3: "",
            self.KEY_DNDLOGD4: "",
            self.KEY_DNDLOGD5: "",
            self.KEY_DNDLOGD6: "",
            self.KEY_DNDLOGD7: "",
            self.KEY_DNDLOGD8: "",
            self.KEY_VOC: "",
            self.KEY_WINDSPEED: "",
            
            self.KEY_PNC_PPLUS: "#/cm³",
            self.KEY_PM2_5_PPLUS: "μg/m³",
            self.KEY_PM10_PPLUS: "μg/m³",
            self.KEY_DNDLOGDP300T350_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP350T400_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP400T450_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP450T500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP500T550_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP550T600_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP600T650_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP650T700_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP700T800_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP800T900_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP900T1000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP1000T1250_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP1250T1500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP1500T2000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP2000T2500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP2500T3000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP3000T3500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP3500T4000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP4000T4500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP4500T5000_PPLUS: "#/cm³",
            self.KEY_DNDLOGD5000T5500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP5500T6000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP6000T6500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP6500T7000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP7000T7500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP7500T8000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP8000T8500_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP8500T9250_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP9250T10000_PPLUS: "#/cm³",
            self.KEY_DNDLOGDP10000T25000_PPLUS: "#/cm³",
            
            self.KEY_TEMPERATURE_HDC3022: "°C",
            self.KEY_HUMIDITY_HDC3022: "%",
            
            self.KEY_NOISELEQ_NSRTMK4: "dB",
            
            self.KEY_ACCELERATION_X: "m/s²",
            self.KEY_ACCELERATION_Y: "m/s²",
            self.KEY_ACCELERATION_Z: "m/s²",
            self.KEY_ACCELERATION_RMS: "m/s²",
            
            self.KEY_TEMPERATURE_DIFFERENCE: "°C",
            self.KEY_BACKGROUND_TEMPERATURE: "°C",
            
            self.KEY_MRT: "°C",
            self.KEY_MRT_DIFFERENCE: "°C",
            self.KEY_MRT_BACKGROUND_DIFFERENCE: "°C",
            
            self.KEY_PHIDGET_TEMPERATURE: "°C",
            
            self.KEY_PET: "°C",
            self.KEY_UTCI: "°C",
            
            self.KEY_POTHOLE: "",
            #self.KEY_POTHOLE_PERMALINK: "",
            
            }
        if units is not None:   # If units are provided, update the default units accordingly
            if isinstance(units, dict):
                for key, value in units.items():
                    self.set_units(key, value)
            else:
                raise TypeError("units must be a dictionary with keys as measurement types and values as their units.")
        self.plotting = {} # Initialize all plotting as linear by default
        for key in self.units.keys():
            if key != self.KEY_LATITUDE and key != self.KEY_LONGITUDE: # Latitude, and longitude are excluded from plotting
                self.plotting[key] = self.default_plotting
        if plotting is not None: # If plotting options are provided, update the default plotting options accordingly
            if isinstance(plotting, dict):
                for key, value in plotting.items():
                    self.set_plotting(key, value)
            else:
                raise TypeError("plotting must be a dictionary with keys representing measured variables and values as 'linear', 'logarithmic', 'diverging', 'utci' or 'hidden' depending on which plotting type is desired.")
        self.tagged_only = {} # Initialize tagged_only as an empty list
        if tagged_only is not None:
            for key, tags in tagged_only.items():
                if key not in self.units:
                    raise KeyError(f"Key '{key}' not found in units.")
                if not isinstance(tags, list):
                    raise TypeError(f"Tags for '{key}' must be provided as a list.")
                self.tagged_only[key] = tags
        self.limits = {} # Initialize limits as an empty dictionary
        if limits is not None: # If limits are provided, update the default limits accordingly
            if isinstance(limits, dict):
                for key, value in limits.items():
                    if isinstance(value, tuple) and len(value) == 2:
                        if isinstance(value[0], (int, float)) and isinstance(value[1], (int, float)):
                            self.set_limits(key, value[0], value[1])
                        else:
                            types = [type(value[0]), type(value[1])]
                            raise TypeError(f"Both limits for {key} must be int or float. Got {types[0]} and {types[1]}.")
                    else:
                        raise TypeError(f"Limits for {key} must be a tuple of length 2.")
            else:
                raise TypeError("Limits must be a dictionary with keys as measurement types and values as tuples with min and max values.")
        self.json_files = json_files
        if self.json_files is not None: # Load data from the provided JSON files if applicable
            self.load_data(json_files)
            if start_time is not None or end_time is not None: # Trim DataFrame according to provided time limits
                self.time_trim(start_time, end_time)    
            if min_lat is not None or max_lat is not None or min_lon is not None or max_lon is not None: # Trim DataFrame according to provided location limits
                self.loc_trim(min_lat, max_lat, min_lon, max_lon)
            if self.tagged_only: # Apply tag filter if applicable
                self.apply_tag_filter()
            if output_json_filename is not None: # If an output filename is provided, output the data to a JSON file
                self.output_data(output_json_filename)
            if output_map_filename is not None: # If an output map filename is provided, plot the data on a map
                self.output_map(output_map=output_map_filename)
        
    def load_data(self, json_files=None):
        """
        Loads data from JSON files into a pandas DataFrame.
        """

        if not isinstance(json_files, list):
            if isinstance(json_files, str):
                json_files = [json_files]
            else:
                raise TypeError("json_files must be a list or string.")

        data = []
        for file in json_files:
            with open(file, 'r') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)

        data = pd.DataFrame(data)
        data[self.KEY_TIME] = pd.to_datetime(data[self.KEY_TIME])

        # FIX: safe DataFrame check
        if self.data is None or self.data.empty:
            self.data = data
        else:
            self.data = pd.concat([self.data, data], ignore_index=True)

        self.convert_to_float()
        
    def apply_tag_filter(self):
        """
        Applies the tag filter to the data based on the tagged_only dictionary.
        """
        if self.data is None:
            raise ValueError("No data loaded.")
        
        df = self.data.copy()
        
        for key, tags in self.tagged_only.items():
            if key not in df.columns:
                raise KeyError(f"Key '{key}' not found in DataFrame columns.")
            mask = ~df[self.KEY_OBSERVATION_TYPE].isin(tags)
            df.loc[mask, key] = np.nan
        
        self.data = df
    
    def create_binned_dataframe(self):
        """
        FIXED: consistent UTM usage + corrected inverse transform.
        """

        if self.data is None:
            raise ValueError("No data loaded.")

        df = self.data.copy()

        # FIX: remove self.transformer usage
        xs, ys = self.to_utm.transform(
            df[self.KEY_LONGITUDE].values,
            df[self.KEY_LATITUDE].values
        )

        df["x"] = xs
        df["y"] = ys

        df["bin_x"] = (df["x"] // self.bin_size_m).astype(int)
        df["bin_y"] = (df["y"] // self.bin_size_m).astype(int)

        group_cols = ["bin_x", "bin_y"]
        groups = df.groupby(group_cols)

        numeric_cols = [
            c for c in df.columns
            if c in self.units
            and c not in [self.KEY_LATITUDE, self.KEY_LONGITUDE, self.KEY_TIME]
        ]

        #binned = df.groupby(group_cols)[numeric_cols].mean().reset_index()
        binned = groups[numeric_cols].mean().reset_index()
        
        binned["cell_id"] = binned["bin_x"].astype(str) + "_" + binned["bin_y"].astype(str)
        
        binned["count"] = groups.size().values
        
        if self.histogram:
            def make_time_data(group):

                out_h = {}

                for day, day_group in group.groupby(group[self.KEY_TIME].dt.date):

                    hours = (
                        day_group[self.KEY_TIME].dt.hour
                        + day_group[self.KEY_TIME].dt.minute/60
                        + day_group[self.KEY_TIME].dt.second/3600
                    )

                    out_h[str(day)] = hours.tolist()

                return out_h
        
            binned["time_data"] = groups.apply(make_time_data).values
            binned["day_counts"] = groups.apply(lambda g: {
                str(d): len(g[g[self.KEY_TIME].dt.date == d])
                for d in g[self.KEY_TIME].dt.date.unique()
            }).values
            
            self.histogram_lookup = {}
            
            for _, row in binned.iterrows():
                self.histogram_lookup[row["cell_id"]] = {
                    "hours": row["time_data"],
                    "days": row["day_counts"]
                }

        binned["x_center"] = (binned["bin_x"] + 0.5) * self.bin_size_m
        binned["y_center"] = (binned["bin_y"] + 0.5) * self.bin_size_m

        # FIX: correct inverse transform
        lon, lat = self.to_wgs.transform(
            binned["x_center"].values,
            binned["y_center"].values
        )

        binned[self.KEY_LATITUDE] = lat
        binned[self.KEY_LONGITUDE] = lon

        self.binned_data = binned
        return binned
    
    def output_data(self, filename:str="output_data.json"):
        """
        Outputs the data into a json file.
        """
        
        if self.data is None: # Check if data is loaded
            raise ValueError("No data loaded. Please load data before outputting.")
        if not isinstance(filename, str): # Ensure filename is a string
            raise TypeError("filename must be a string representing the output file name.")
        if not filename.endswith('.json'): # Ensure the filename ends with .json
            filename += '.json'
        self.data.to_json(filename, orient="records", date_format="iso", indent=4) # Output the data to a JSON file with ISO date format and pretty print
    
    def set_units(self, key:str, new_unit:str):
        """
        Sets the units for a given variable.
        """
        
        if not isinstance(key, str):
            raise TypeError("Key must be a string representing the measurement type.")
        if key in self.units and key != self.KEY_TIME:
            self.units[key] = new_unit
        else:
            if key == self.KEY_TIME:
                raise ValueError("Time unit cannot be changed.")
            else:
                raise KeyError(f"Key '{key}' not found in units.")
        
    def set_limits(self, key:str, min_value:float=None, max_value:float=None):
        """
        Sets the limits for a given variable. If min_value or max_value is None, that limit will not be altered.
        """
        
        if not isinstance(key, str):
            raise TypeError("Key must be a string representing the measurement type.")
        if not isinstance(min_value, (int, float, type(None))) or not isinstance(max_value, (int, float, type(None))):
            raise TypeError("min_value and max_value must be numbers or None.")
        if key == self.KEY_TIME:
            raise ValueError("Limits cannot be set for time. Data should instead be filtered based on measurement time using the time_trim method instead or by giving the time limits using the 'start_time' and 'end_time' variables while creating the MobileMeasurementMapper instance.")
        if key not in self.limits:
            self.limits[key] = {}
        if min_value is not None:
            self.limits[key]["min"] = min_value
        if max_value is not None:
            self.limits[key]["max"] = max_value

    def set_plotting(self, key:str, plotting_type:str):
        """
        Sets the plotting type for a given variable. Possible options are 'linear', 'logarithmic', 'diverging', 'utci', 'discrete', or 'hidden'.
        """
        
        if not isinstance(key, str):
            raise TypeError("Keys in plotting must be strings representing measurement types.")
        if key == self.KEY_TIME or key == self.KEY_LATITUDE or key == self.KEY_LONGITUDE: # Time, latitude, and longitude are excluded from plotting
            raise ValueError(f"Plotting for {key} is not supported.")
        if plotting_type == "linear" or plotting_type == "logarithmic" or plotting_type == "diverging" or plotting_type == "utci" or plotting_type == "discrete" or plotting_type == "hidden": # Check if value is a valid plotting type
            self.plotting[key] = plotting_type
        else:
            raise ValueError(f"Plotting options for {key} must be either 'linear', 'logarithmic', 'diverging', 'utci', 'discrete', or 'hidden'.")
                    
    def time_trim(self, start_time=None, end_time=None):
        """
        Trims the data based on given start and end time.
        """
        
        if self.data is None: # Check if data is loaded
            raise ValueError("No data loaded. Please load data before trimming.")
        if start_time is not None:
            if isinstance(start_time, str):
                start_time = pd.to_datetime(start_time)
            elif not isinstance(start_time, pd.Timestamp):
                raise TypeError("start_time must be a string or a pandas Timestamp.")
        if end_time is not None:
            if isinstance(end_time, str):
                end_time = pd.to_datetime(end_time)
            elif not isinstance(end_time, pd.Timestamp):
                raise TypeError("end_time must be a string or a pandas Timestamp.")
        if start_time and end_time:
            self.data = self.data[(self.data[self.KEY_TIME] >= start_time) & (self.data[self.KEY_TIME] <= end_time)]
        elif start_time:
            self.data = self.data[self.data[self.KEY_TIME] >= start_time]
        elif end_time:
            self.data = self.data[self.data[self.KEY_TIME] <= end_time]

    def loc_trim(self, min_lat:float=None, max_lat:float=None, min_lon:float=None, max_lon:float=None):
        """
        Trims the data based on given latitude and longitude limits.
        """
        
        if self.data is None: # Check if data is loaded
            raise ValueError("No data loaded. Please load data before trimming.")
        if min_lat is not None:
            if not isinstance(min_lat, (int, float)):
                raise TypeError("min_lat must be a number.")
            self.data = self.data[self.data[self.KEY_LATITUDE] >= min_lat]
        if max_lat is not None:
            if not isinstance(max_lat, (int, float)):
                raise TypeError("max_lat must be a number.")
            self.data = self.data[self.data[self.KEY_LATITUDE] <= max_lat]
        if min_lon is not None:
            if not isinstance(min_lon, (int, float)):
                raise TypeError("min_lon must be a number.")
            self.data = self.data[self.data[self.KEY_LONGITUDE] >= min_lon]
        if max_lon is not None:
            if not isinstance(max_lon, (int, float)):
                raise TypeError("max_lon must be a number.")
            self.data = self.data[self.data[self.KEY_LONGITUDE] <= max_lon]

    def get_min_max(self, key: str, output: bool=False):
        """
        Returns the minimum and maximum values for the given key.
        """
        
        if not isinstance(key, str):
            raise TypeError("Key must be a string representing a variable.")
        if key not in self.data.columns: # Check if the variable exists in the data
            raise KeyError(f"Key '{key}' not found in data.")
        binned = self.create_binned_dataframe()
        min_value = binned[key].min() # Get the minimum value for the variable
        max_value = binned[key].max() # Get the maximum value for the variable
        if key in self.limits: # Check if limits are set for the variable and adjust min and max values accordingly
            if "min" in self.limits[key]:
                min_value = max(min_value, self.limits[key]["min"])
            if "max" in self.limits[key]:
                max_value = min(max_value, self.limits[key]["max"])
        self.min_max[key] = (min_value, max_value) # Store the min and max values in the min_max dictionary
        if output: # If output is True, return the min and max values
            return min_value, max_value
    
    def cmap(self, key: str, value: float):
        """
        Returns a color based on the value of the variable given as the key using a colormap.
        """
        
        plotting_type = self.plotting.get(key) # Get the plotting type for the variable
        if plotting_type == "diverging":
            #colormap = mpl.colormaps.get_cmap("coolwarm")
            #colormap = mpl.colormaps.get_cmap("bwr")
            colormap = mpl.colormaps.get_cmap("seismic")
        else:
            colormap = mpl.colormaps.get_cmap("jet")

        if key not in self.data.columns: # Check if the variable exists in the data
            raise KeyError(f"Key '{key}' not found in data.")
        plotting_type = self.plotting.get(key) # Get the plotting type for the variable
        min_value, max_value = self.min_max.get(key, (None, None)) # Get the minimum and maximum values for the variable
        if min_value is None or max_value is None: # If min and max values are not set, calculate them
            self.get_min_max(key)
            min_value, max_value = self.min_max[key]
        if plotting_type not in ["discrete", "utci"]: # If plotting type is not discrete or utci, check if value is within the min and max values
            if value < min_value: # If value is below the minimum value, set plotting value to 0
                value = min_value
            elif value > max_value:
                value = max_value
        if max_value == min_value: # If min and max values are the same, set plotting value to 0
                plotting_value = 0
                warnings.warn(f"Min and max values for key '{key}' are the same ({min_value}). Setting plotting value to 0.")
                
        elif plotting_type == "linear": 
            plotting_value = (value - min_value) / (max_value - min_value) # Calculate the plotting value for linear plotting
            
        elif plotting_type == "logarithmic":
            plotting_value = math.log(1+(math.exp(1)-1)*(value-min_value)/(max_value-min_value)) # Calculate the plotting value for logarithmic plotting
            
        elif plotting_type == "diverging":
            vmax = max(abs(min_value), abs(max_value))
            plotting_value = (value + vmax) / (2 * vmax) # Calculate the plotting value for diverging plotting
            
        elif plotting_type == "utci":
            if key not in self.utci_supported_keys:
                raise ValueError(f"Key '{key}' is not supported for UTCI plotting.")
            utci_category = self.utci[self.utci[0] >= value].index[0] # Get the UTCI category for the value
            plotting_value = self.utci.loc[utci_category][0] # Get the UTCI value for the category
            return self.utci.loc[utci_category][1] # Return the color for the UTCI category
        
        elif plotting_type == "discrete":
            if key == self.KEY_NUMBER:
                discrete_values = self.naneos_number_discrete
            elif key == self.KEY_PM2_5_PPLUS:
                discrete_values = self.pm2_5_discrete
            elif key == self.KEY_PM10_PPLUS:
                discrete_values = self.pm10_discrete
            elif key == self.KEY_ACCELERATION_RMS:
                discrete_values = self.rms_acceleration_discrete
            else:
                raise ValueError(f"Key '{key}' is not supported for discrete plotting.")
            discrete_category = discrete_values[discrete_values[0] >= value].index[0] # Get the discrete category for the value
            plotting_value = discrete_values.loc[discrete_category][0] # Get the discrete value for the category
            return discrete_values.loc[discrete_category][1] # Return the color for the discrete category
            
        elif plotting_type == "hidden":
            raise ValueError(f"Plotting for key '{key}' is set to 'hidden'. Cannot calculate color for hidden variables.")
        
        else:
            raise ValueError(f"Invalid plotting type '{plotting_type}' for key '{key}'.")
        
        return mpl.colors.rgb2hex(colormap(float(plotting_value))) # Convert the plotting value to a hex color code using the colormap
    
    def convert_to_float(self): 
        """
        Converts all columns in the DataFrame to float type, except for the time column.
        """
        
        if self.data is None: # Check if data is loaded
            raise ValueError("No data loaded. Please load data before converting to float.")
        for key in self.units.keys():
            if key != self.KEY_TIME and key != self.KEY_POTHOLE_PERMALINK: # Dont convert time and permalink
                if key in self.data.columns:
                    try:
                        self.data[key] = self.data[key].astype(float)
                    except ValueError as e:
                        raise ValueError(f"Could not convert column '{key}' to float: {e}")
    
    def get_legend_values(self, key: str):
        """
        Returns a list of legend values for the given key based on the plotting type.
        """
        
        if not isinstance(key, str): # Ensure key is a string
            raise TypeError("Key must be a string representing a variable.")
        if key not in self.data.columns: # Check if the variable exists in the data
            raise KeyError(f"Key '{key}' not found in data.")
        plotting_type = self.plotting.get(key) # Get the plotting type for the variable
        self.get_min_max(key) # Ensure min and max values are set for the variable
        min_value = self.min_max[key][0] # Get the minimum value for the variable
        max_value = self.min_max[key][1] # Get the maximum value for the variable
        if plotting_type == "linear": # If plotting type is linear, create legend values based on linear interpolation
            return [min_value, 
                    min_value * 3/4 + max_value * 1/4,
                    min_value * 1/2 + max_value * 1/2, 
                    min_value * 1/4 + max_value * 3/4, 
                    max_value
                    ]
        elif plotting_type == "logarithmic": # If plotting type is logarithmic, create legend values based on logarithmic interpolation
            return [min_value,
                    (math.exp(1/4)-1)/(math.exp(1)-1)*(max_value-min_value)+min_value, 
                    (math.exp(1/2)-1)/(math.exp(1)-1)*(max_value-min_value)+min_value,
                    (math.exp(3/4)-1)/(math.exp(1)-1)*(max_value-min_value)+min_value,
                    max_value
                    ]
        elif plotting_type == "diverging": # If plotting type is diverging, create legend values based on diverging interpolation
            vmax = max(abs(min_value), abs(max_value))
            return [-vmax, -vmax/2, 0, vmax/2, vmax]
        
        elif plotting_type == "utci": # If plotting type is utci, create legend values based on utci categories
            if key not in self.utci_supported_keys:
                raise ValueError(f"Key '{key}' is not supported for UTCI plotting.")
            legend_values = list(self.utci[self.utci[0] >= min_value][0])[:5]
            if len(legend_values) < 5:
                legend_values = list(self.utci[-5:][0])
            return legend_values
        
        elif plotting_type == "discrete": # If plotting type is discrete, create legend values based on discrete categories
            if key == self.KEY_NUMBER:
                discrete_values = self.naneos_number_discrete
            elif key == self.KEY_PM2_5_PPLUS:
                discrete_values = self.pm2_5_discrete
            elif key == self.KEY_PM10_PPLUS:
                discrete_values = self.pm10_discrete
            elif key == self.KEY_ACCELERATION_RMS:
                discrete_values = self.rms_acceleration_discrete
            else:
                raise ValueError(f"Key '{key}' is not supported for discrete plotting.")
            legend_values = list(discrete_values[0])
            return legend_values
            
        elif plotting_type == "hidden":
            raise ValueError(f"Plotting for key '{key}' is set to 'hidden'. Cannot calculate legend values for hidden variables.")
        else:
            raise ValueError(f"Invalid plotting type '{plotting_type}' for key '{key}'.")
        
    def get_present_data(self):
        """
        Returns a list with the currently present data keys with plotting enabled.
        """
        
        if self.data is None: # Check if data is loaded
            raise ValueError("No data loaded. Please load data before getting present data.")
        present_data = []
        for key in self.plotting.keys():
            if key in self.data.columns and self.data[key].notna().any():
                present_data.append(key)
        return present_data
        
    def create_layer(self, keys):
        """
        Creates layers for the map based on the provided keys.
        """
        
        if not isinstance(keys, list): # Ensure keys is a list
            if isinstance(keys, str):
                keys = [keys]
            else:
                raise TypeError("keys must be a list of strings representing variables or a single string representing a variable.")  
        present_data = self.get_present_data() # Get the currently present data keys 
        for key in keys: # Check if the provided keys are valid
            if key == self.KEY_LATITUDE or key == self.KEY_LONGITUDE or key == self.KEY_TIME:
                raise ValueError(f"Plotting for {key} is not supported.")
            elif key not in present_data: # Check if the variable exists in the data
                raise KeyError(f"Key '{key}' not found in data.")
            elif key not in self.plotting: # Check if the key is in the plotting options
                raise KeyError(f"Key '{key}' not found in plotting options.")  
        if self.map is None: # If map is not initialized, create a new folium map centered at the mean latitude and longitude of the data
            self.map = folium.Map(location=[self.data[self.KEY_LATITUDE].mean(), self.data[self.KEY_LONGITUDE].mean()], zoom_start=self.starting_zoom, tiles="OpenStreetMap")
        for key in keys: # Create layers
            legend_values = self.get_legend_values(key) # Get the legend values for the variable
            unit = self.units[key] # Get the unit for the variable
            layer = folium.FeatureGroup(name=f"{key} ({self.plotting[key]}) <br><font color='{self.cmap(key, legend_values[0])}'> •</font> = {legend_values[0]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[1])}'> •</font> = {legend_values[1]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[2])}'> •</font> = {legend_values[2]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[3])}'> •</font> = {legend_values[3]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[4])}'> •</font> = {legend_values[4]:.2f} {unit} ",
                                                   control=True,
                                                   show=False 
                                                   ).add_to(self.map)
            self.layers[key] = layer      
        
    def create_layer_control(self):
        """
        Creates a layer control for the map to change visible layer.
        """
        
        if self.map is None: # Check if map is created
            raise ValueError("No map created. Please create a map using either create_layer or plot_map before creating a layer control.")
        layer_group = []
        for layer in self.layers.values(): # Collect all layers into a layergroup
            layer_group.append(layer)
        folium.plugins.GroupedLayerControl(collapsed=True, 
                                           draggable=True, 
                                           groups={"Maps": layer_group}
                                           ).add_to(self.map) # Add the layer control to the map
        
    def create_pothole_marker_layer(self, cluster_size_m=50):
        """
        Creates one marker per pothole cluster.

        Detections within cluster_size_m of each other are grouped
        into a single marker. The popup contains all associated images.
        """

        if self.data is None:
            raise ValueError("No data loaded.")

        if self.map is None:
            raise ValueError("Map must be initialized before adding pothole markers.")

        layer = folium.FeatureGroup(
            name=f"{self.KEY_POTHOLE}_detections",
            show=True
        )

        # -----------------------------------------
        # Filter pothole detections
        # -----------------------------------------

        df = self.data[
        #    (self.data[self.KEY_POTHOLE] == 1)
            (self.data[self.KEY_POTHOLE] > 0)
            & self.data[self.KEY_LATITUDE].notna()
            & self.data[self.KEY_LONGITUDE].notna()
        ].copy()

        if len(df) == 0:
            layer.add_to(self.map)
            self.layers["pothole_markers"] = layer
            return

        # -----------------------------------------
        # Convert to projected coordinates (meters)
        # -----------------------------------------

        x, y = self.to_utm.transform(
            df[self.KEY_LONGITUDE].values,
            df[self.KEY_LATITUDE].values
        )

        df["x"] = x
        df["y"] = y

        # -----------------------------------------
        # Create clustering bins
        # -----------------------------------------

        df["cluster_x"] = (df["x"] // cluster_size_m).astype(int)
        df["cluster_y"] = (df["y"] // cluster_size_m).astype(int)

        groups = df.groupby(["cluster_x", "cluster_y"])

        # -----------------------------------------
        # Create one marker per cluster
        # -----------------------------------------

        for _, group in groups:

            lat = group[self.KEY_LATITUDE].mean()
            lon = group[self.KEY_LONGITUDE].mean()

            detection_count = int(group[self.KEY_POTHOLE].sum())

            all_urls = []
            timestamps = []

            for _, row in group.iterrows():

                timestamps.append(row.get(self.KEY_TIME, ""))

                urls = row.get(self.KEY_POTHOLE_PERMALINK, [])

                if isinstance(urls, list):
                    all_urls.extend(urls)
                elif urls:
                    all_urls.append(urls)

            html = f"""
            <div style="width:280px;height:500px;overflow-y:auto;">
                <b>Road surface damage detections:</b> {detection_count}<br>
                <hr>
            """

            for url in all_urls:

                html += f"""
                <a href="{url}" target="_blank">
                    <img
                        src="{url}"
                        style="
                            width:250px;
                            border:1px solid #ccc;
                            margin-bottom:10px;
                        ">
                </a>
                """

            html += "</div>"

            popup = folium.Popup(
                folium.IFrame(
                    html=html,
                    width=320,
                    height=550
                ),
                max_width=350
            )

            tooltip = f"{detection_count} pothole detections"

            folium.Marker(
                location=(lat, lon),
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(
                    color="red",
                    icon="warning-sign"
                )
            ).add_to(layer)

        layer.add_to(self.map)

        self.layers["pothole_markers"] = layer
        
    def add_pothole_heatmap(self):
        """
        Adds a pothole heatmap layer.
        Uses raw detections (denser, noisier)
        """

        if self.map is None:
            raise ValueError("Map must be initialized before adding heatmap.")

        df = self.data

        heat_data = [
            [row[self.KEY_LATITUDE], row[self.KEY_LONGITUDE], 1]
            for _, row in df.iterrows()
            if row.get(self.KEY_POTHOLE, 0) == 1
        ]

        name = "Pothole heatmap"

        heat_layer = folium.FeatureGroup(name=name, show=False)

        HeatMap(
            heat_data,
            radius=15,
            blur=20,
            max_zoom=18,
        ).add_to(heat_layer)

        self.layers[f"{self.KEY_POTHOLE}_heatmap"] = heat_layer
        heat_layer.add_to(self.map)
        
    def add_pothole_heatmap_binned(self):
        """
        Adds a pothole heatmap layer.
        Uses binned averaged pothole probability (cleaner).
        """

        if self.map is None:
            raise ValueError("Map must be initialized before adding heatmap.")

        
        df = self.create_binned_dataframe()

        if self.KEY_POTHOLE not in df.columns:
            raise ValueError(f"No '{self.KEY_POTHOLE}' column in data.")

        heat_data = [
            [row[self.KEY_LATITUDE], row[self.KEY_LONGITUDE], row[self.KEY_POTHOLE]]
            for _, row in df.iterrows()
            if not pd.isna(row[self.KEY_POTHOLE]) and row[self.KEY_POTHOLE] > 0
        ]

        name = "Pothole heatmap (binned)"

        heat_layer = folium.FeatureGroup(name=name, show=False)

        HeatMap(
            heat_data,
            radius=15,
            blur=20,
            max_zoom=18,
        ).add_to(heat_layer)
        

        self.layers[f"{self.KEY_POTHOLE}_heatmap_binned"] = heat_layer
        heat_layer.add_to(self.map)
        
    def add_observation_layers(self, cluster_size_m=50):
        """
        Creates a marker layer for each observation type.
        
        On each layer, creates one marker per observation cluster.

        Detections within cluster_size_m of each other are grouped
        into a single marker. The popup contains all associated images.
        """
        
        
        
        if self.data is None:
            raise ValueError("No data loaded.")

        if self.map is None:
            raise ValueError("Map must be initialized before adding pothole markers.")
        
        observation_types = self.data[self.KEY_OBSERVATION_TYPE].dropna().unique()
        
        route = self.data[[self.KEY_LATITUDE, self.KEY_LONGITUDE]].dropna().values.tolist()
        
        for observation_type in observation_types:
            
            observation_layer = folium.FeatureGroup(
                        name=f"{observation_type}_observations",
                        show=True
                    )
            
            # -----------------------------------------
            # Filter observations
            # -----------------------------------------
            
            df = self.data[
                (self.data[self.KEY_OBSERVATION_TYPE] == observation_type)
                & self.data[self.KEY_LATITUDE].notna()
                & self.data[self.KEY_LONGITUDE].notna()
            ].copy()
            
            if len(df) == 0:
                observation_layer.add_to(self.map)
                self.layers[f"{observation_type}_observations"] = observation_layer
                continue
            
            # -----------------------------------------
            # Convert to projected coordinates (meters)
            # -----------------------------------------
            
            x, y = self.to_utm.transform(
                df[self.KEY_LONGITUDE].values,
                df[self.KEY_LATITUDE].values
            )
            
            df["x"] = x
            df["y"] = y
            
            # -----------------------------------------
            # Create clustering bins
            # -----------------------------------------
            
            if cluster_size_m <= 0:
                # No clustering
                df["cluster_x"] = df["x"]
                df["cluster_y"] = df["y"]
            else:
                df["cluster_x"] = (df["x"] // cluster_size_m).astype(int)
                df["cluster_y"] = (df["y"] // cluster_size_m).astype(int)
            
            groups = df.groupby(["cluster_x", "cluster_y"])
            
            # -----------------------------------------
            # Draw route
            # -----------------------------------------
            
            if len(route) > 1:
                folium.PolyLine(
                    locations=route,
                    color="black",
                    weight=3,
                    opacity=0.8,
                ).add_to(observation_layer)
            
            # -----------------------------------------
            # Create one marker per cluster
            # -----------------------------------------
            
            for _, group in groups:
                
                lat = group[self.KEY_LATITUDE].mean()
                lon = group[self.KEY_LONGITUDE].mean()
                
                detection_count = len(group)
                
                tooltip = f"{detection_count} {observation_type} observation"
                if detection_count > 1:
                    tooltip += "s"
                
                folium.Marker(
                    location=(lat, lon),
                    tooltip=tooltip,
                    icon=folium.Icon(
                        color="blue",
                        icon="info-sign"
                    )
                ).add_to(observation_layer)
                
            observation_layer.add_to(self.map)
            
            self.layers[f"{observation_type}_observations"] = observation_layer
            
        
    def make_histogram_popup(self, cell_id):

        div_id = f"hist_{uuid.uuid4().hex}"

        return f"""
                    <div class="histogram-popup"
                        data-cell="{cell_id}"
                        data-canvas="{div_id}"
                        data-select="{div_id}_select"
                        style="width:500px">

                        <select id="{div_id}_select"></select>

                        <canvas id="{div_id}"
                                width="450"
                                height="250"></canvas>

                    </div>
                """
        
    def output_map(self, keys=None, output_map="output_map.html"):
        """
        Creates a binned folium map where each grid cell represents mean values.
        """
        
        half = self.bin_size_m / 2

        if self.data is None:
            raise ValueError("No data loaded.")

        binned = self.create_binned_dataframe()

        if keys is None:
            keys = self.get_present_data()

        if self.map is None:
            self.map = folium.Map(
                location=[binned[self.KEY_LATITUDE].mean(),
                        binned[self.KEY_LONGITUDE].mean()],
                zoom_start=self.starting_zoom,
                tiles="OpenStreetMap"
            )
            
        if self.histogram:

            self.map.get_root().html.add_child(
                folium.Element(f"""
                <script>
                    window.histogramLookup = {json.dumps(self.histogram_lookup)};
                </script>
                """)
            )
            
            self.map.get_root().html.add_child(
                folium.Element("""
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                """)
            )
            
            self.map.get_root().html.add_child(
                folium.Element("""
            <script>

            // ======================================================
            // 1. Histogram logic (defined ONCE)
            // ======================================================

            function makeHistogram(hours) {

                const counts = new Array(24).fill(0);

                hours.forEach(function(h) {
                    const i = Math.floor(h);
                    if (i >= 0 && i < 24) {
                        counts[i]++;
                    }
                });

                return counts;
            }

            function drawHistogram(canvasID, selectID, data) {

                const canvas = document.getElementById(canvasID);
                const select = document.getElementById(selectID);

                if (!canvas || !select || !data) return;

                const labels = [];
                for (let i = 0; i < 24; i++) {
                    labels.push(String(i).padStart(2, "0") + ":00");
                }

                //--------------------------------------------------
                // Build dropdown
                //--------------------------------------------------

                const keys = [
                    "by date",
                    "by hour (all dates)",
                    ...Object.keys(data.hours)
                ];

                select.innerHTML = "";

                keys.forEach(function(k) {
                    const option = document.createElement("option");
                    option.value = k;
                    option.text = k;
                    select.appendChild(option);
                });

                //--------------------------------------------------
                // Combined hourly data
                //--------------------------------------------------

                const allHours = [];

                Object.values(data.hours).forEach(function(arr) {
                    allHours.push(...arr);
                });

                //--------------------------------------------------

                const ctx = canvas.getContext("2d");
                let chart = null;

                function draw(selection) {

                    if (chart) {
                        chart.destroy();
                    }

                    //--------------------------------------------------
                    // Counts by date
                    //--------------------------------------------------

                    if (selection === "by date") {

                        const days = Object.keys(data.days);

                        chart = new Chart(ctx, {
                            type: "bar",
                            data: {
                                labels: days,
                                datasets: [{
                                    label: "Measurements per day",
                                    data: days.map(d => data.days[d])
                                }]
                            },
                            options: {
                                responsive: false,
                                animation: false,
                                scales: {
                                        x: {
                                            title: {
                                                display: true,
                                                text: "Date (UTC)"
                                            }
                                        },
                                        y: {
                                            beginAtZero: true,
                                            title: {
                                                display: true,
                                                text: "Number of measurements"
                                            }
                                        }
                                    }
                            }
                        });

                        return;
                    }

                    //--------------------------------------------------
                    // Hour distribution using ALL dates
                    //--------------------------------------------------

                    if (selection === "by hour (all dates)") {

                        chart = new Chart(ctx, {
                            type: "bar",
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: "Measurements from all days",
                                    data: makeHistogram(allHours)
                                }]
                            },
                            options: {
                                responsive: false,
                                animation: false,
                                scales: {
                                        x: {
                                            title: {
                                                display: true,
                                                text: "Time of day (UTC)"
                                            }
                                        },
                                        y: {
                                            beginAtZero: true,
                                            title: {
                                                display: true,
                                                text: "Number of measurements"
                                            }
                                        }
                                    }
                            }
                        });

                        return;
                    }

                    //--------------------------------------------------
                    // Individual day
                    //--------------------------------------------------

                    chart = new Chart(ctx, {
                        type: "bar",
                        data: {
                            labels: labels,
                            datasets: [{
                                label: "Measurements from " + selection,
                                data: makeHistogram(data.hours[selection])
                            }]
                        },
                        options: {
                            responsive: false,
                            animation: false,
                                scales: {
                                        x: {
                                            title: {
                                                display: true,
                                                text: "Time of day (UTC)"
                                            }
                                        },
                                        y: {
                                            beginAtZero: true,
                                            title: {
                                                display: true,
                                                text: "Number of measurements"
                                            }
                                        }
                                    }
                        }
                    });
                }

                select.onchange = function() {
                    draw(select.value);
                };

                draw("by date");
            }


            // ======================================================
            // 2. Leaflet popup binding (SAFE + LATE)
            // ======================================================

            function initHistogramBinding() {

                const mapObject = Object.values(window).find(v =>
                    v && v._leaflet_id
                );

                if (!mapObject) {
                    console.warn("Leaflet map not found yet");
                    return;
                }

                mapObject.on("popupopen", function(e) {

                    setTimeout(() => {

                        const popup = e.popup.getElement();
                        if (!popup) return;

                        const div = popup.querySelector(".histogram-popup");
                        if (!div) return;

                        const cell = div.dataset.cell;
                        const data = window.histogramLookup?.[cell];

                        if (!data) {
                            console.warn("No histogram data for cell:", cell);
                            return;
                        }

                        drawHistogram(
                            div.dataset.canvas,
                            div.dataset.select,
                            data
                        );

                    }, 50);

                });
            }


            // ======================================================
            // 3. Wait for full page load
            // ======================================================

            window.addEventListener("load", function() {
                initHistogramBinding();
            });

            </script>
            """)
            )

        #for key in keys:
        for key in tqdm(keys, desc="Layers", total=len(keys), unit="layer"):
            if key not in binned.columns or self.plotting.get(key) == "hidden":
                continue
            
            unit = self.units.get(key, "")
            legend_values = self.get_legend_values(key)
            
            if self.plotting.get(key) == "utci" and key in self.utci_supported_keys:
                legend_categories = [self.utci[self.utci[0] >= v].index[0] for v in legend_values]
                temperature_intervals = []
                for category in legend_categories:
                    idx = self.utci.index.get_loc(category)
                    if idx == 0:
                        # First category: no previous category
                        temperature_intervals.append(f"(< {legend_values[0]} {unit})")
                    elif idx == len(self.utci) - 1:
                        # Last category: no next category
                        temperature_intervals.append(f"(≥ {legend_values[-2]} {unit})")
                    else:
                        previous_threshold = self.utci.iloc[idx - 1, 0]
                        current_threshold = self.utci.iloc[idx, 0]
                        temperature_intervals.append(
                            f"({previous_threshold}–{current_threshold} {unit})"
                        )
                legend = f"{key} ({self.plotting[key]}) <br>"
                for i, category in enumerate(legend_categories):
                    legend += f"<font color='{self.cmap(key, legend_values[i])}'> •</font> = {category} {temperature_intervals[i]} <br>"
            elif self.plotting.get(key) == "discrete":
                if key == self.KEY_NUMBER:
                    discrete_values = self.naneos_number_discrete
                elif key == self.KEY_PM2_5_PPLUS:
                    discrete_values = self.pm2_5_discrete
                elif key == self.KEY_PM10_PPLUS:
                    discrete_values = self.pm10_discrete
                elif key == self.KEY_ACCELERATION_RMS:
                    discrete_values = self.rms_acceleration_discrete
                else:
                    raise ValueError(f"Key '{key}' is not supported for discrete plotting.")
                if key == self.KEY_ACCELERATION_RMS:
                    legend = f"{key} ({self.plotting[key]}) <br><font color='{self.cmap(key, legend_values[0])}'> •</font> < {discrete_values.iloc[0, 0]} {unit} <br><font color='{self.cmap(key, legend_values[1])}'> •</font> ≥ {discrete_values.iloc[0, 0]} {unit} "
                else:
                    legend = f"{key} ({self.plotting[key]}) <br><font color='{self.cmap(key, legend_values[0])}'> •</font> < {discrete_values.iloc[0, 0]} {unit} <br><font color='{self.cmap(key, legend_values[1])}'> •</font> {discrete_values.iloc[0, 0]}–{discrete_values.iloc[1, 0]} {unit} <br><font color='{self.cmap(key, legend_values[2])}'> •</font> {discrete_values.iloc[1, 0]}–{discrete_values.iloc[2, 0]} {unit} <br><font color='{self.cmap(key, legend_values[3])}'> •</font> ≥ {discrete_values.iloc[2, 0]} {unit} "
            else:
                legend = f"{key} ({self.plotting[key]}) <br><font color='{self.cmap(key, legend_values[0])}'> •</font> = {legend_values[0]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[1])}'> •</font> = {legend_values[1]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[2])}'> •</font> = {legend_values[2]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[3])}'> •</font> = {legend_values[3]:.2f} {unit} <br><font color='{self.cmap(key, legend_values[4])}'> •</font> = {legend_values[4]:.2f} {unit} "
            
            self.legends[key] = legend
            layer = folium.FeatureGroup(name=key,
                                        control=True,
                                        show=False 
                                        )
            self.layers[key] = layer

            self.get_min_max(key)  # ensure scaling
            
            #for row in binned.itertuples():
            for row in tqdm(binned.itertuples(), desc=f"Plotting {key}", total=len(binned), unit="point"):
                value = getattr(row, key)

                if pd.isna(value):
                    continue

                #folium.CircleMarker(
                #    location=(getattr(row, self.KEY_LATITUDE),
                #            getattr(row, self.KEY_LONGITUDE)),
                #    radius=5,
                #    color=self.cmap(key, value),
                #    fill=True,
                #    fill_opacity=0.8,
                #    tooltip=f"{key}: {value:.2f}",
                #).add_to(layer)

                # center in meters
                cx = row.x_center
                cy = row.y_center

                # 4 corners in meter space
                corners_m = [
                    (cx - half, cy - half),
                    (cx + half, cy - half),
                    (cx + half, cy + half),
                    (cx - half, cy + half),
                ]
                
                lon, lat = self.to_wgs.transform(
                    [c[0] for c in corners_m],
                    [c[1] for c in corners_m]
                )

                polygon = list(zip(lat, lon))

                #folium.Polygon(
                #    locations=polygon,
                #    color=self.cmap(key, value),
                #    fill=True,
                #    fill_opacity=0.5,
                #    weight=0.5,
                #    tooltip=f"{key}: {value:.2f}"
                #).add_to(layer)
                
                popup = None
                
                if self.histogram:
                    popup = folium.Popup(
                        self.make_histogram_popup(row.cell_id),
                       max_width=550
                    )
                
                tooltip = f"{key}: {value:.2f}"
                if self.display_counts:
                    tooltip += f"<br>n = {row.count}"
                
                folium.Polygon(
                    locations=polygon,
                    color=self.cmap(key, value),
                    fill=True,
                    fill_opacity=0.75,
                    weight=0.5,
                    tooltip=tooltip,
                    popup=popup
                ).add_to(layer)

            layer.add_to(self.map)

        if self.KEY_POTHOLE in keys:
            self.create_pothole_marker_layer()
        #self.add_pothole_heatmap()
        #self.add_pothole_heatmap_binned()
        
        #if self.KEY_OBSERVATION_TYPE in keys:
        
        self.add_observation_layers(cluster_size_m=0)
            
        self.create_layer_control()
        folium.plugins.Fullscreen().add_to(self.map)
        
        legend_json = json.dumps(self.legends)
        legend_html = f"""
        <div id="legend-box"
            style="
                position: fixed;
                bottom: 30px;
                left: 30px;
                z-index:9999;
                background:white;
                border:2px solid gray;
                border-radius:5px;
                padding:10px;
                max-width:260px;
                font-size:13px;
                box-shadow:2px 2px 5px rgba(0,0,0,0.3);
        ">
        No layer selected
        </div>

        <script>

        const legends = {legend_json};

        </script>
        """

        self.map.get_root().html.add_child(
            folium.Element(legend_html)
        )
        
        script = """
        <script>

        window.addEventListener("load", function(){

            function updateLegend(){

                // Find the checked radio button or checkbox
                const checked = document.querySelector(
                    ".leaflet-control-layers input:checked"
                );

                if(!checked)
                    return;

                // The layer name is stored in the accompanying label
                const label = checked.parentElement.textContent.trim();

                const box = document.getElementById("legend-box");

                if(label in legends)
                    box.innerHTML = legends[label];
                else
                    box.innerHTML = "";
            }

            //--------------------------------------------------------
            // Wait until LayerControl exists
            //--------------------------------------------------------

            setTimeout(function(){

                const controls = document.querySelectorAll(
                    ".leaflet-control-layers input"
                );

                controls.forEach(function(control){

                    control.addEventListener("change", updateLegend);

                });

                updateLegend();

            },500);

        });

        </script>
        """

        self.map.get_root().html.add_child(
            folium.Element(script)
        )

        if not output_map.endswith(".html"):
            output_map += ".html"

        self.map.save(output_map)


#m = MobileMeasurementMapper(json_files="2025-05-07.json", output_map_filename="test_map.html")
#m = MobileMeasurementMapper(json_files="2025-05-07.json", output_json_filename="test_2.json")