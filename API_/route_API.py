import googlemaps
from datetime import datetime
from polyline import decode
from math import sqrt

from typing import Tuple, Dict, List


class RouteAPI:
    __gmaps : googlemaps.Client
    __API_key : str

    __DEFAULT_DISTANCE_BETWEEN_POINTS : int = 50000
    __REGION : str = "NL"
    __MODE : str = "driving"

    def __init__(self, API_key: str):
        self.__API_key = API_key
        self.__gmaps = googlemaps.Client(self.__API_key)

    def get_routes(self, origin: str | Dict | Tuple | List, destination: str | Dict | Tuple | List,
                   alternatives: bool = False) -> List[Dict]:
        """
        Get route(s) from origin to destination.
        List of routes can be empty if there is no route between origin and destination.

        Args:
            origin (str | Dict | Tuple | List): The address or latitude/longitude value from which you wish to calculate directions.
            destination (str | Dict | Tuple | List): The address or latitude/longitude value from which you wish to calculate directions.
            alternatives (bool, optional): If True, more than one route may be returned in the response. Defaults to False.

        Returns:
            List[Dict]: list of calculated route(s) from origin to destination.
        """
        
        raw_routes = self.__gmaps.directions(
            origin,
            destination,
            alternatives=alternatives,
            departure_time=datetime.now(),
            mode=self.__MODE,
            region=self.__REGION)

        routes = [self.__parse_route(raw_route) for raw_route in raw_routes]

        return routes

    def get_duration_and_distance(self, origin: str | Dict | Tuple | List, destination: str | Dict | Tuple | List) -> Dict | None:
        """
        Get duration and distance of route from origin to destination.
        Light version of get_routes for the cases when only duration and distance must be calculated.

        Args:
            origin (str | Dict | Tuple | List): The address or latitude/longitude value from which you wish to calculate directions.
            destination (str | Dict | Tuple | List): The address or latitude/longitude value from which you wish to calculate directions.

        Returns:
            Dict | None: Dictionary with duration (in seconds) and distance (in meters) from origin to destination.
            If there is no route from destination to origin, None is returned.
        """
        
        raw_routes = self.__gmaps.directions(
            origin,
            destination,
            departure_time=datetime.now(),
            mode=self.__MODE,
            region=self.__REGION)

        duration_and_distance = None

        if len(raw_routes) > 0:
            leg = raw_routes[0]["legs"][0]

            duration_and_distance = {
                "distance": leg["distance"]["value"],
                "distance_text": leg["distance"]["text"],
                "duration": leg["duration"]["value"],
                "duration_text": leg["duration"]["text"],
            }

        return duration_and_distance
    
    def get_stop_points(self, route: Dict, distance_between_points: int = __DEFAULT_DISTANCE_BETWEEN_POINTS,
                        traveled_distance: int = 0) -> List[Dict]:
        """
        Calculate points on the route with indicated distance between each other.

        Args:
            route (Dict): Route from origin to destination.
            distance_between_points (int, optional): Distnace between points on the route (in meters).
            Defaults to __DEFAULT_DISTANCE_BETWEEN_POINTS.
            traveled_distance (int, optional): Distance which was passed by driver (in meters).
            Defaults to 0.
        
        Returns:
            List[Dict]: list of points on the route.
            Point consists of dictionary which contains lattitude, longtitude and distance (in meters) on the route.
            Distance is not entirely precise. Some diviation from reality is possible due to calculatation in float point numbers.
        """
        
        points = list()
        
        full_distance = 0
        distance = traveled_distance % distance_between_points
        
        for step in route["steps"]:
            distance += step["distance"]
            full_distance += step["distance"]

            if distance >= distance_between_points:
                new_points, distance = self.__aproximate_stop_points(
                    step, distance, distance_between_points, full_distance)
                points.extend(new_points)

        return points
    
    def predict_point_on_route(self, route: Dict, coordinate: Dict, next_point_distance: int) -> Dict | None:
        """Not completed!!!!"""
        
        predicted_point: Dict | None = None
        step_ind: int | None = self.__locate_step(route["steps"], coordinate)
        
        if step_ind is not None:
            to_end_current_step_route = self.get_routes(coordinate, route["steps"][step_ind]["end_location"])
            
            if len(to_end_current_step_route) > 0:
                left_steps : List[Dict] = to_end_current_step_route[0]["steps"] + route["steps"][step_ind + 1:]              
                distance : int = 0
                full_distance : int = 0
                            
                for step in left_steps:
                    distance += step["distance"]
                    full_distance += step["distance"]
                    
                    if distance >= next_point_distance:
                        new_points, _ = self.__aproximate_stop_points(
                            step, distance, next_point_distance, full_distance, only_first=True)
                        
                        predicted_point = new_points[0]
                        break
                
                if predicted_point is None and distance < next_point_distance and len(left_steps) > 0:
                    predicted_point = self.__init_stop_point(
                        left_steps[-1]["end_location"]["lat"], left_steps[-1]["end_location"]["lng"],
                        distance)
        
        return predicted_point       
        
        
    def __locate_step(self, steps: List[Dict], coordinate: Dict) -> int | None:
        step_ind: int | None = None
        min_double_length: float = float("inf")
        
        for ind, step in enumerate(steps):
            
            double_length : float = 0.0
            
            for x, y in (
                (step["start_location"]["lat"], step["start_location"]["lng"]),
                (step["end_location"]["lat"], step["end_location"]["lng"])):
                
                x_length : float = x - coordinate["lat"]
                y_length : float = y - coordinate["lng"]
                double_length += sqrt(x_length**2 + y_length**2)
            
            if double_length < min_double_length:
                min_double_length = double_length
                step_ind = ind
        
        return step_ind
            
        
    @staticmethod
    def __calculate_sector_lengths(coordinates: List) -> Tuple[List, float]:
        polyline_length = 0.0
        sector_lengths = list()
        
        for ind in range(0, len(coordinates) - 1):
            x_sector_length = coordinates[ind][0] - coordinates[ind+1][0]
            y_sector_length = coordinates[ind][1] - coordinates[ind+1][1]
            sector_length = sqrt(x_sector_length**2 + y_sector_length**2)
            
            sector_lengths.append(sector_length)
            polyline_length += sector_length
        
        return sector_lengths, polyline_length
    
    @staticmethod
    def __init_stop_point(lat: float, lng: float, distance: int) -> Dict:
        stop_point = {
                "lat" : lat,
                "lng" : lng,
                "distance" : distance,
            }
        
        return stop_point
        
    @classmethod
    def __aproximate_stop_points(cls, step: Dict, distance : int, distance_between_points: int,
                                  full_distance: int, only_first: bool = False) -> Tuple[List[Dict], int]:
        
        points = list()
        new_distance = 0
        coordinates = decode(step["polyline"])
        
        if step["distance"] > 0 and len(coordinates) > 0:
            sector_lengths, polyline_length = cls.__calculate_sector_lengths(coordinates)
            
            first_stop_point_percent = abs(distance_between_points - (distance - step["distance"])) / step["distance"]
            next_stop_point_percent = distance_between_points / step["distance"]
                    
            current_polyline = 0.0
            current_percent = first_stop_point_percent
            stop_point_on_polyline = first_stop_point_percent * polyline_length
            next_stop_point_length = next_stop_point_percent * polyline_length
            
            for ind, sector_length in enumerate(sector_lengths):
                current_polyline += sector_length
                
                if current_polyline > stop_point_on_polyline:
                    points.append(cls.__init_stop_point(
                        coordinates[ind][0], coordinates[ind][1],
                        full_distance - step["distance"] + int(current_percent * step["distance"])))
                    
                    current_percent += next_stop_point_percent
                    stop_point_on_polyline += next_stop_point_length
                    new_distance = full_distance - points[-1]["distance"]
                    
                    if only_first:
                        break
            
        if len(points) == 0:
            points.append(
                cls.__init_stop_point(step["end_location"]["lat"], step["end_location"]["lng"], full_distance))
        
        return points, new_distance

    @staticmethod
    def __parse_route(raw_route: Dict) -> Dict:
        route = dict()
        
        route["bounds"] = raw_route["bounds"]
        
        leg = raw_route["legs"][0]
    
        route["start_address"] = leg["start_address"]
        route["start_location"] = leg["start_location"]
        route["end_address"] = leg["end_address"]
        route["end_location"] = leg["end_location"]

        route["distance"] = leg["distance"]["value"]
        route["distance_text"] = leg["distance"]["text"]
        route["duration"] = leg["duration"]["value"]
        route["duration_text"] = leg["duration"]["text"]

        route["steps"] = list()
        for raw_step in leg["steps"]:
            step = dict()

            step["start_location"] = raw_step["start_location"]
            step["end_location"] = raw_step["end_location"]
            step["distance"] = raw_step["distance"]["value"]
            step["duration"] = raw_step["duration"]["value"]
            step["polyline"] = raw_step["polyline"]["points"]

            route["steps"].append(step)

        route["polyline"] = raw_route['overview_polyline']["points"]

        return route