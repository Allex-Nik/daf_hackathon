import os
import sys
import googlemaps # library for Google Maps API. Use 'pip install googlemaps' to install

# Modifying the root path for imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import API_.route_API as route_API # file with class RouteAPI
from geopy.distance import geodesic


class PlacesNearby:
    """Class for interacting with Google Maps API 
    to get places nearby given coordinates, radius and types of places."""

    def __init__(self, api_key: str):
        """Initializes the class with the API key."""
        self.gmaps = googlemaps.Client(key=api_key)
        self.places = []
        self.shortlist = []
        self.route_object = route_API.RouteAPI(API_key=api_key)


    def get_places(self, lat: float, lng: float, radius: int, types: list[str]) -> list[dict]:
        """Given coordinates, radius and types, retrieves objects within a certain radius
         :param lat: latitude
         :param lng: longitude
         :param radius: radius
         :param types: list of types of places (fast_food_restaurant, coffee_shop and so on)
         :return: list of dictionaries with keys 'distance', 'name', 'rating', 'vicinity' and 'location'
         A full list of supported types: 
         https://developers.google.com/maps/documentation/places/web-service/place-types"""

        places = []

        for place_type in types:
            query_result = self.gmaps.places_nearby(
                location=(lat, lng),
                radius=radius,
                #max_price=4,
                type=place_type)

            for place in query_result.get('results', []):
                place_info = {
                    'name' : place.get('name', 'No name'), 
                    'rating' : place.get('rating', 'No rating'), 
                    'vicinity' : place.get('vicinity', 'No vicinity'), # address
                    'location' : place.get('geometry', {}).get('location', 'No location'), # dict with keys 'lat' and 'lng'
                    'distance' : self.route_object.get_duration_and_distance(
                        (lat, lng), (place.get('geometry', {}).get('location', 'No location')))['distance'],
                    'price_level' : place.get('price_level', 'No price level')
                }
                places.append(place_info) # places is a list of dictionaries

        # remove duplicates
        unique_places = {f"{place['name']} | {place['location']['lat']} | {place['location']['lng']}": place for place in places} 
        
        self.places = list(unique_places.values())

        # remove places that are further than radius
        self.places = [place for place in self.places if geodesic(
            (lat, lng), (place['location']['lat'], place['location']['lng'])).meters <= radius]
        
        # removes places with price level higher than 2
        self.places = [place for place in self.places 
                       if (isinstance(place['price_level'], int) and place['price_level'] <= 2) 
                       or place['price_level'] == 'No price level']

        return self.places
    

    def make_shortlist(self) -> list[dict]:
        """Given a list of places, returns a shortlist of the 3 closest places.
        :param places: list of dictionaries with keys 'name', 'rating', 'vicinity' and 'location'
        :return: list of dictionaries with keys 'distance', 'name', 'rating', 'vicinity' and 'location'"""

        closest_places = sorted(self.places, key=lambda x: x['distance'])[:3]

        return closest_places


# Example run
if __name__ == '__main__':
    import pprint
    import pandas as pd

    df = pd.read_pickle("C:\\Users\\20232179\\Desktop\\Study\\Quarter4\\daf\\dummy.pkl")

    api_key = 'AIzaSyBhboakcvUvt3yxTlf5Tlt9LQ-wIqLrQS4' # New key supporting Places API (New). We will need to hide it later
    client = PlacesNearby(api_key=api_key)

    # Run for a range of rows

    # for i in range (150, 170):
    #     lat = df.iloc[i]['snapshotData_gnssPosition_latitude']
    #     lng = df.iloc[i]['snapshotData_gnssPosition_longitude']

    #     radius = 5000
    #     types = ['restaurant', 'bed_and_breakfast', 'rest_stop', 'cafe', 'hostel', 'motel', 'truck_stop', 'parking']
    #     places = client.get_places(lat, lng, radius, types)
    #     shortlist = client.make_shortlist()
    #     pprint.pprint(shortlist)

    # Run for a single row
    
    lat = df.iloc[0]['snapshotData_gnssPosition_latitude']
    lng = df.iloc[0]['snapshotData_gnssPosition_longitude']

    radius = 500
    types = ['restaurant', 'bed_and_breakfast', 'rest_stop', 'cafe', 'hostel', 'motel', 'truck_stop', 'parking']
    places = client.get_places(lat, lng, radius, types)
    shortlist = client.make_shortlist()
    pprint.pprint(shortlist)
    print(lat)
    print(lng)

    # Example output
#   [{'distance': 75,
#   'location': {'lat': 51.79345679999999, 'lng': 4.619109999999999},
#   'name': "Dutch Harbor 's-Gravendeel BV",
#   'rating': 4.3,
#   'vicinity': "Griendweg 14, 's-Gravendeel"},
#  {'distance': 307,
#   'location': {'lat': 51.79170990000001, 'lng': 4.615400000000001},
#   'name': 'AFVALBOX v.o.f.',
#   'rating': 'No rating',
#   'vicinity': "Griendweg 41, 's-Gravendeel"},
#  {'distance': 308,
#   'location': {'lat': 51.791677, 'lng': 4.615365},
#   'name': 'Carré Karton B.V.',
#   'rating': 4.7,
#   'vicinity': "Griendweg 41, 's-Gravendeel"}]
