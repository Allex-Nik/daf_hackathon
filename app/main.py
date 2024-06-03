import os 
import sys 
import folium
import polyline
import streamlit as st

from folium import PolyLine
from streamlit_folium import folium_static

# Modifying the root path for imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent) 

from config import API_KEY
from API_.route_API import RouteAPI

# Initialize the RouteAPI
route_API = RouteAPI(API_KEY)

# Streamlit page configuration
st.set_page_config(
    layout='wide'
)

# Streamlit sidebar inputs for origin and destination
st.sidebar.title("Route Planner")
origin = st.sidebar.text_input("Origin", "Delft")
destination = st.sidebar.text_input("Destination", "Groningen")

# # Fetch coordinates for the destination (if needed)
# destination_coords = route_API.get_coordinates(destination)

# Get route
routes = route_API.get_routes(origin, destination)

# The best route choice
route = routes[0] 

# Get stop points within 50km
stop_points = route_API.get_stop_points(route, 50000)

# Remove steps from the route dictionary
route.pop("steps")


# Decode the polyline string
polyline_str = str(route['polyline'])
coordinates = polyline.decode(polyline_str)

# Create a Folium map centered around the midpoint of the coordinates
midpoint = len(coordinates) // 2
map_center = coordinates[midpoint]
map_ = folium.Map(location=map_center, zoom_start=8)

# Add the polyline to the map
polyline_layer = PolyLine(locations=coordinates, color='blue', weight=5)
map_.add_child(polyline_layer)

# Display the map in Streamlit
st.title("Route Map")

# Display the map 
folium_static(map_, width=1200, height=750)
