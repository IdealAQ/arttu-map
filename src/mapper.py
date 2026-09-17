#from mobile_average_mapper_v2_4 import MobileMeasurementMapper
#from mobile_average_mapper_v2_4_potholes import MobileMeasurementMapper
#from mobile_average_mapper_v2_6_custom_cmaps import MobileMeasurementMapper
#from mobile_average_mapper_v2_7 import MobileMeasurementMapper
#from mobile_average_mapper_v2_8 import MobileMeasurementMapper
#from mobile_average_mapper_v2_8_presentation import MobileMeasurementMapper
from mobile_average_mapper_v2_9 import MobileMeasurementMapper




#date = "2026-04-14_1_with_potholes_with_temp_diff"
#date = "2026-05-14_with_rms"
#date = "2026-06-30_trimmed"
#date = "2026-06-30_with_rms_with_temp_diff_with_mrt_diff_tagged"
#date = "Mazara_del_Vallo_slim"
#date = "Mazara_del_Vallo_stationary_with_pet_and_utci_trimmed"
#date = "Mazara_del_Vallo_with_temp_diff_with_mrt_diff_trimmed"
#date = "Mazara_del_Vallo_with_temp_diff_with_mrt_diff_with_pet_and_utci_trimmed"
#date = "Helsinki_summer_2026/all_data_with_rms_with_temp_diff_trimmed"
#date = "Tarto_2026_full_with_filtered_rms"
#date = "Tarto_2026_full_presentation_2026-04-15"
date = "Parnu/all_data_2026-08_processed"
bin_size_m = 20
display_counts = True
histogram = False #True
limits = {
            "airsence_co_ppb": (200, 600),
            "airsence_co2_ppm": (420, 500),
            #"airsence_humamb_x": (0, 50),
            #"airsence_lux_xx": (100, 3500),
            "airsence_no_ppb": (0, 7.5),
            "airsence_no2_ppb": (0, 25),
            "airsence_noiseleq_db": (55, 85),
            "airsence_o3_ppb": (0, 50),
            "alphopc_pm1p0_ugm3": (0, 10),
            "alphopc_pm2p5_ugm3": (0, 25),
            "alphopc_pm10p0_ugm3": (0, 100),
            "airsence_pressureamb_x": (1025.68, 1040),
            "airsence_so2_ppb": (0, 25),
            #"airsence_tempamb_x": (25, 35),
            #"airsence_voc_ppm": (60, 100),
            "airsence_voc_ppm": (75, 150),
            #"naneos_number": (0, 100000),
            "naneos_diameter": (0, 100),
            "naneos_ldsa": (0, 100),
            "naneos_total_surface_area": (0, 500),
            #"naneos_geom_std_dev": (1.75, 2.5),
            "naneos_geom_std_dev": (1.75, 3),
            #"naneos_dNdlogD1": (25000, 75000),
            "naneos_dNdlogD1": (0, 75000),
            "naneos_dNdlogD2": (0, 75000),
            "naneos_dNdlogD3": (0, 75000),
            "naneos_dNdlogD4": (0, 75000),
            "naneos_dNdlogD5": (0, 75000),
            "naneos_dNdlogD6": (0, 75000),
            "naneos_dNdlogD7": (0, 75000),
            "naneos_dNdlogD8": (0, 75000),
            #"pplus_pnc_ptcm3": (0, 50),
            "pplus_pnc_ptcm3": (0, 150),
            #"pplus_pm2p5_ugm3": (0, 25),
            #"pplus_pm10_ugm3": (0, 100),
            #"pplus_dNdlogdP300to350nm_ptcm3": (0, 0.05), 
            "pplus_dNdlogdP300to350nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP350to400nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP400to450nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP450to500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP500to550nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP550to600nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP600to650nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP650to700nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP700to800nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP800to900nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP900to1000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP1000to1250nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP1250to1500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP1500to2000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP2000to2500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP2500to3000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP3000to3500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP3500to4000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP4000to4500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP4500to5000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP5000to5500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP5500to6000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP6000to6500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP6500to7000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP7000to7500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP7500to8000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP8000to8500nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP8500to9250nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP9250to10000nm_ptcm3": (0, 0.1),
            "pplus_dNdlogdP10000to25000nm_ptcm3": (0, 0.1),
            #"hdc3022_temp_c": (0, 0),
            #"hdc3022_rh_pct": (0, 0),
            #"nsrtmk4_noiseleq_db": (75, 100),
          }
#limits = {}
default_plotting = "logarithmic"
#plotting_exceptions = {}
plotting_exceptions = {#"scanwai_pothole": "hidden",
#                       #"airsence_windspeed_xx": "linear",
                       "hdc3022_temp_c": "linear",
#                       #"hdc3022_temp_c": "utci",
                       "hdc3022_rh_pct": "linear",#"utci",
                       "background_temp_c": "linear",
#                       #"background_temp_c": "utci",
                       "mrtmax31865_temp_c": "linear",
#                       #"mrtmax31865_temp_c": "utci",
#                       #"pet_c": "utci",
#                       #"utci_c": "utci", 
                       "phidget_temp_c": "linear",
                       "temp_diff_c": "diverging",
                       "MRT_airtemp_diff_c": "diverging",
                       "MRT_airtemp_diff_background_c": "diverging",
                       "nsrtmk4_noiseleq_db": "linear",
                       "naneos_number": "discrete",
                       "pplus_pm2p5_ugm3": "discrete",
                       "pplus_pm10_ugm3": "discrete", 
                       "imu_rms_acceleration": "discrete",
#                       "scanwai_pothole": "hidden",
                       }
#plotting_exceptions = {
    #"PM2.5": "discrete",
    #"PM10": "discrete",
    #"Temperature": "linear",
    #"Temperature Difference to Reference Station": "diverging",
    #"Relative Humidity": "linear",
    #"PM2.5": "discrete",
    #"PM10": "discrete",
    #"Surface Damage": "hidden",
    #"Surface Roughness": "discrete",
#}
    
    
tags = {
  #"airsence_windspeed_xx": ["manhole_cover"],
  #"pet_c": ["manhole_cover"],
  #"utci_c": ["manhole_cover"]
}



input_json_file = f"{date}.json"
output_json_file = f"data_{date}.json"
output_map_file = f"map_{date}.html"



m = MobileMeasurementMapper(json_files=[input_json_file],
                            output_json_filename=output_json_file,
                            output_map_filename=output_map_file,
                            limits=limits,
                            plotting=plotting_exceptions,
                            default_plotting=default_plotting,
                            bin_size_m=bin_size_m,
                            histogram=histogram,
                            display_counts=display_counts,
                            #tagged_only=tags
                            )