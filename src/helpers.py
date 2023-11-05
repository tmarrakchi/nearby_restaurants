import math
import json
import argparse
import time
from src.point import Point
from src.restaurant import Restaurant

# Function to calculate the Haversine distance between two points
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000  # Convert seconds to milliseconds
        print(f"Function '{func.__name__}' took {elapsed_time_ms:.2f} ms to execute.")
        return result
    return wrapper

class Helpers:
    def haversine(self, point1, point2):
        # Radius of the Earth in meters (6,371km)
        earth_radius = 6371000

        # Convert latitude and longitude from degrees to radians (trigonometric functions)
        lat1, lon1 = map(math.radians, [point1.latitude, point1.longitude])
        lat2, lon2 = map(math.radians, [point2.latitude, point2.longitude])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Calculate the distance in meters
        distance = round(earth_radius * c, 2)

        return distance

    # Search for restaurants within a specified radius of the centroid
    @log_time
    def find_restaurants(self, centroid_point, radius, restaurants):
        nearby_restaurants = []

        for restaurant in restaurants["features"]:
            restaurant_lat = restaurant["geometry"]["coordinates"][1]
            restaurant_lon = restaurant["geometry"]["coordinates"][0]
            restaurant_point = Point(restaurant_lat, restaurant_lon)

            distance = self.haversine(centroid_point, restaurant_point)

            if distance <= radius:
                restaurant_name = restaurant["properties"]["name"]
                nearby_restaurants.append(Restaurant(restaurant_name, restaurant_lat, restaurant_lon, distance))

        return nearby_restaurants

    # Load the restaurant data from the JSON file
    @log_time
    def load_restaurants(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def get_args(self):
        parser = argparse.ArgumentParser(description="Find nearby restaurants")
        parser.add_argument("--latitude", type=float, required=True, help="Latitude of the centroid")
        parser.add_argument("--longitude", type=float, required=True, help="Longitude of the centroid")
        parser.add_argument("--radius", type=float, required=True, help="Search radius in meters")

        args = parser.parse_args()
        return args
