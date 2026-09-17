import panel as pn
import folium

# CRITICAL FIX: You must include 'folium' inside the extension!
pn.extension('folium')

# 1. Setup a Selector Widget
city_selector = pn.widgets.Select(
    name='Select City', 
    options={
        'Helsinki': [60.1699, 24.9384], 
        'New York': [40.7128, -74.0060]
    }
)

# 2. Define the Map Generation Logic
def generate_map(coordinates):
    # Create the raw Folium map
    f_map = folium.Map(location=coordinates, zoom_start=12)
    folium.Marker(location=coordinates, popup="Selected Location").add_to(f_map)
    
    # Return it wrapped explicitly in Panel's Folium pane
    return pn.pane.plot.Folium(f_map, sizing_mode='stretch_both', min_height=500)

# 3. CRITICAL FIX: Bind the function and wrap it with pn.panel
# This ensures Panel establishes a proper HTML container for the map layout
interactive_map = pn.panel(
    pn.bind(generate_map, city_selector), 
    sizing_mode='stretch_both'
)

# 4. Layout and Serve
app = pn.Column(
    "# Cloud-Data Folium Map",
    city_selector,
    interactive_map,
    sizing_mode='stretch_both'
)

app.servable()