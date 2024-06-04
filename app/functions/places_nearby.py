
# Given coordinates, radius and types, connects to Google Maps API and
# returns names of the objects, their rating, address and coordinates

import googlemaps # library for Google Maps API. Use 'pip install googlemaps' to install

class PlacesNearby:
    """Class for interacting with Google Maps API to get places nearby given coordinates, radius and types of places."""

    def __init__(self, api_key: str):
        """Initializes the class with the API key."""
        self.gmaps = googlemaps.Client(key=api_key)

    def get_places(self, lat: float, lng: float, radius: int, types: list[str]) -> list[dict]:
        """Given coordinates, radius and types, retrieves objects within a certain radius
         :param lat: latitude
         :param lng: longitude
         :param radius: radius
         :param types: list of types of places (fast_food_restaurant, coffee_shop and so on)
         A full list of supported types: https://developers.google.com/maps/documentation/places/web-service/place-types"""

        places = []

        for place_type in types:
            query_result = self.gmaps.places_nearby(
                location=(lat, lng),
                radius=radius,
                type=place_type)

            for place in query_result.get('results', []):
                place_info = {
                    'name' : place.get('name', 'No name'), 
                    'rating' : place.get('rating', 'No rating'), 
                    'vicinity' : place.get('vicinity', 'No vicinity'), # address
                    'location' : place.get('geometry', {}).get('location', 'No location') # dict with keys 'lat' and 'lng'
                }
                places.append(place_info) # places is a list of dictionaries with keys 'name', 'rating', 'vicinity' and 'location'

        unique_places = {f"{place['name']} | {place['location']['lat']} | {place['location']['lng']}": place for place in places} # removes duplicates
        
        return list(unique_places.values())

# We can also implement opening hours given the expected time of arrival




# Example run
if __name__ == '__main__':
    import pprint
    import pandas as pd

    df = pd.read_pickle("C:\\Users\\20232179\\Desktop\\Study\\Quarter4\\daf\\dummy.pkl")

    api_key = 'AIzaSyBhboakcvUvt3yxTlf5Tlt9LQ-wIqLrQS4' # New key supporting Places API (New). We will need to hide it later
    client = PlacesNearby(api_key=api_key)

    for i in range (150, 170):
        lat = df.iloc[i]['snapshotData_gnssPosition_latitude']
        lng = df.iloc[i]['snapshotData_gnssPosition_longitude']

        radius = 50
        types = ['restaurant', 'bed_and_breakfast', 'rest_stop', 'cafe', 'hostel', 'motel', 'truck_stop', 'parking']
        places = client.get_places(lat, lng, radius, types)
        pprint.pprint(places)

    # Example output

    # [{'location': {'lat': 51.5591638, 'lng': 5.090805599999999},
    #   'name': 'Restaurant Agora',
    #   'rating': 4.4,
    #   'vicinity': 'Heuvelring 33, Tilburg'},
    #  {'location': {'lat': 51.55897299999999, 'lng': 5.0911785},
    #   'name': 'Mo-Jo sushi en grill Japanese kitchen',
    #   'rating': 4,
    #   'vicinity': 'Heuvelring 90, Tilburg'},
    #  {'location': {'lat': 51.56021, 'lng': 5.092058799999999},
    #   'name': 'Aim Aroy',
    #   'rating': 4.1,
    #   'vicinity': 'NS-Plein 10, Tilburg'},
    #  {'location': {'lat': 51.5589981, 'lng': 5.0906653},
    #   'name': 'De Heuvel Chicken',
    #   'rating': 3,
    #   'vicinity': 'Heuvelring 39b, Tilburg'}]
