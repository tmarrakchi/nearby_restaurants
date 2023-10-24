# Restaurant Finder

Restaurant Finder is a Python application that helps you find nearby restaurants within a specified radius of a centroid point. This application uses Haversine distance to calculate the distance between coordinates and searches for restaurants within the given radius.

## Prerequisites

Before you can run the Restaurant Finder application, make sure you have the following prerequisites installed on your system:

- Python 3

## Usage

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the `main.py` script with the required arguments:


Replace `<centroid_latitude>`, `<centroid_longitude>`, and `<search_radius>` with your desired values.

Example:
python main.py --latitude 48.8566 --longitude 2.3522 --radius 1000


4. The application will load restaurant data, perform a query search, and display nearby restaurants along with their names, coordinates, and distances.

## Data Source

Restaurant data is loaded from a GeoJSON file located in the `src/data` directory. You can replace this file with your own data if needed.

## Authors

- Tarik Marrakchi

Enjoy finding restaurants with Restaurant Finder!
