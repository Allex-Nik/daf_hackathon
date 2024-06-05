from route_API import RouteAPI
from test_route import route

API_key = "AIzaSyA2jyZ5RD-g9n1Mb-56Oi1BgYUVRPkwXHs"

#You need to create RouteAPI to init google maps Client
route_API = RouteAPI(API_key)

# Coordinate of city close to Groningen (lattitude, longtitude)
# city_coordinate = (53.10493223076839, 6.881467967781942)

# Get route
route = route_API.get_routes("Venlo", "Zwolle")[0]


# Get stop points within 50km
stop_points = route_API.get_stop_points(route, 50000,  traveled_distance = 30000)

coordinate = {
    "lat" : 51.58789853806958,
    "lng" : 5.977947176270335,
}

predicted_stop_point_1 = route_API.get_point_on_route(route, coordinate, distance=100000)
predicted_stop_point_2 = route_API.get_point_on_route(route, coordinate, time=5000, speed=20)


print("ROUTE DICTIONARY")
print(route)
print("____________________")

print("STOP POINTS")
print(stop_points)
print("____________________")

print("PREDICTED_POINT")
print(predicted_stop_point_1)
print(predicted_stop_point_2)
print("____________________")


#Calculate only distnace.
# print(route_API.get_duration_and_distance("Delft", "Zwickau, Germany"))