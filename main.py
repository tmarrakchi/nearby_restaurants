import time
import os
from src.helpers import Helpers as H

if __name__ == "__main__":
    
    args = H.get_args()
    centroid_lat = args.latitude
    centroid_lon = args.longitude
    radius = args.radius

    # Record the start time for data loading
    start_time_data_loading = H.get_time()

    # Load restaurant data
    current_folder = os.path.dirname(os.path.abspath(__file__))
    restaurants = H.load_restaurants(f"{current_folder}/src/data/restaurants_paris.geojson")

    # Calculate the time taken for data loading
    data_loading_time_ms = H.get_time(start_time_data_loading)

    # Record the start time for query search
    start_query_search_time = H.get_time()

    # Find nearby restaurants
    nearby_restaurants = H.find_restaurants(centroid_lat, centroid_lon, radius, restaurants)

    # Calculate the time taken for query search
    query_search_time_ms = H.get_time(start_time_data_loading)

    # Print the results
    for restaurant in nearby_restaurants:
        print(
            f"name:{restaurant['name']},longitude:{restaurant['longitude']},latitude:{restaurant['latitude']},distance:{restaurant['distance']}"
        )

    print("-------------------------------------------------")
    print(f"Data loading time: {data_loading_time_ms:.2f} ms")
    print(f"Query search time: {query_search_time_ms:.2f} ms")
