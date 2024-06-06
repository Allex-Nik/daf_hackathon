from route_API import RouteAPI

API_key = 'AIzaSyAqyVQ3IW56ZzbyazmCepgYGb4vETOf0V4'

# You need to create RouteAPI to init google maps Client
route_API = RouteAPI(API_key)

#coordinate of city close to Groningen (lattitude, longtitude)
city_coordinate = (53.10493223076839, 6.881467967781942)

#Get route
routes = route_API.get_routes("Delft", city_coordinate)

route = routes[0]

#Get stop points within 50km
stop_points = route_API.get_stop_points(route, 50000)

#I removed steps because I want to print dictionary of route. Steps take too much space.
#Steps are sections of the road.
route.pop("steps")

print("ROUTE DICTIONARY")
print(route)
print("____________________")

print("STOP POINTS")
print(stop_points)
print("____________________")


#Calculate only distnace.
print(route_API.get_duration_and_distance("Delft", "Zwickau, Germany"))