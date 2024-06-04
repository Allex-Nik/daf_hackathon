import os 
import sys 
import folium
import polyline
import streamlit as st

from folium import PolyLine, Marker, Icon
from streamlit_folium import folium_static

# Modifying the root path for imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from config import API_KEY
from API_.route_API import RouteAPI
from functions.places_nearby import PlacesNearby

# Initialize the RouteAPI
route_API = RouteAPI(API_KEY)

# Initialize the PlacesNearby
places_API = PlacesNearby(API_KEY)

# Streamlit page configuration
st.set_page_config(
    layout='wide'
)

# Streamlit sidebar inputs for origin and destination
st.sidebar.title("Route Planner")
type_ = st.sidebar.text_input("Place", "Cafe")
origin = st.sidebar.text_input("Origin", "Technische Universiteit Eindhoven")
destination = st.sidebar.text_input("Destination", "DAF Museum")

# # Fetch coordinates for the destination (if needed)
# destination_coords = route_API.get_coordinates(destination)

# Get route
routes = route_API.get_routes(origin, destination)

# The best route choice
route = routes[0] 

# Get stop points within 50km
stop_points = route_API.get_stop_points(route, 500)

# get the list of places 
place_list = [places_API.get_places(lat=dict_['lat'], lng=dict_['lng'], radius=1000, types=[type_]) for dict_ in stop_points][0]

# Remove steps from the route dictionary
route.pop("steps")

# Decode the polyline string
polyline_str = str(route['polyline'])
coordinates = polyline.decode(polyline_str)

# Create a Folium map centered around the midpoint of the coordinates
midpoint = len(coordinates) // 2
map_center = coordinates[midpoint]
map_ = folium.Map(location=map_center, zoom_start=14)

# Add the polyline to the map
polyline_layer = PolyLine(locations=coordinates, color='blue', weight=5)
map_.add_child(polyline_layer)

# Add markers for each cafe
for cafe in place_list:
    cafe_name = cafe['name']
    cafe_location = cafe['location']
    lat = cafe_location['lat']
    lng = cafe_location['lng']
    
    # Create a marker with a custom icon
    marker = Marker(
        location=[lat, lng],
        popup=cafe_name,
        icon=Icon(icon='coffee', prefix='fa', color='red')  # Customize the icon here
    )
    map_.add_child(marker)

# Display the map in Streamlit
st.title("Route Map")

# Display the map 
folium_static(map_, width=1200, height=750)
