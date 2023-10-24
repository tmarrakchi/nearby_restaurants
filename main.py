import time
import os
from src.helpers import Helpers

if __name__ == "__main__":
    
    helpers = Helpers()
    args = helpers.get_args()
    centroid_lat = args.latitude
    centroid_lon = args.longitude
    radius = args.radius

    # Load restaurant data
    current_folder = os.path.dirname(os.path.abspath(__file__))
    restaurants = helpers.load_restaurants(f"{current_folder}/src/data/restaurants_paris.geojson")

    # Find nearby restaurants
    nearby_restaurants = helpers.find_restaurants(centroid_lat, centroid_lon, radius, restaurants)

    # Print the results
    for restaurant in nearby_restaurants:
        print(
            f"name:{restaurant['name']},longitude:{restaurant['longitude']},latitude:{restaurant['latitude']},distance:{restaurant['distance']}"
        )
