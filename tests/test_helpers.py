import os
import math
import pytest
import json
import argparse
import time
from unittest.mock import patch
from src.helpers import Helpers as H

@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected_distance", [
    (0, 0, 0, 0, 0),                  # Distance entre les mêmes points doit être 0
    (0, 0, 0, 90, 10007539),         # Distance entre le Point A et le Point B
    (90, 0, 0, 0, 10001966),         # Distance entre le Point B et le Point A
    (0, 0, 0, 180, 20015078),        # Distance entre deux points opposés sur la Terre
])
def test_haversine(lat1, lon1, lat2, lon2, expected_distance):
    result = H.haversine(lat1, lon1, lat2, lon2)
    assert math.isclose(result, expected_distance, rel_tol=1e-2)

# Créer des données de test pour les restaurants
restaurants_data = {
    "type": "FeatureCollection",
    "name": "restau_paris",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
    "features": [
        {
            "type": "Feature",
            "properties": { "name": "Restaurant X" },
            "geometry": { "type": "Point", "coordinates": [2.0, 48.0] }
        },
        {
            "type": "Feature",
            "properties": { "name": "Restaurant Y" },
            "geometry": { "type": "Point", "coordinates": [2.1, 48.1] }
        },
        {
            "type": "Feature",
            "properties": { "name": "Restaurant Z" },
            "geometry": { "type": "Point", "coordinates": [2.2, 48.2] }
        }
    ]
}

def test_find_restaurants():
    centroid_lat = 48.0
    centroid_lon = 2.0
    radius = 100  # Plus petit rayon pour inclure uniquement Restaurant X

    result = H.find_restaurants(centroid_lat, centroid_lon, radius, restaurants_data)

    # Vérifier que seul Restaurant X est inclus dans le résultat
    assert len(result) == 1

    # Vérifier les détails de Restaurant X
    restaurant_x = result[0]
    assert restaurant_x["name"] == "Restaurant X"
    assert restaurant_x["latitude"] == 48.0
    assert restaurant_x["longitude"] == 2.0
    assert math.isclose(restaurant_x["distance"], 0.0, rel_tol=1e-2)

def test_load_restaurants():
    # Créer un fichier JSON temporaire avec des données de test
    expected = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": { "name": "Restaurant A" },
                "geometry": { "type": "Point", "coordinates": [2.0, 48.0] }
            },
            {
                "type": "Feature",
                "properties": { "name": "Restaurant B" },
                "geometry": { "type": "Point", "coordinates": [2.1, 48.1] }
            }
        ]
    }
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = f"{current_folder}/data/test_restaurants.json"
    with open(test_file, "w", encoding="utf-8") as file:
        json.dump(expected, file)

    # Charger les restaurants à partir du fichier
    result_data = H.load_restaurants(test_file)

    # Vérifier que les données chargées sont égales aux données de test
    assert result_data == expected

def test_get_args():
    # liste d'arguments simulée
    test_args = ["--latitude", "48.8319929", "--longitude", "2.3245488", "--radius", "100"]

    # patch pour simuler la passation des paramètres en tant qu'arguments
    with patch("sys.argv", ["my_script.py"] + test_args):
        args = H.get_args()

    # Vérifier que les valeurs d'argument sont correctes
    assert args.latitude == 48.8319929
    assert args.longitude == 2.3245488
    assert args.radius == 100

def test_get_time():
    start_time = H.get_time()

    time.sleep(0.1)  # Attendre 100 millisecondes

    end_time = H.get_time(start_time)

    # Vérifier que le temps écoulé est d'environ 100 millisecondes (ou 100 000 microsecondes)
    assert abs(end_time - 100) < 30  # Tolérance de 30 ms pour l'imprécision des délais

    # Vérifier que le temps de départ n'est pas égal au temps actuel (en millisecondes)
    current_time = H.get_time()
    assert current_time != start_time

    # Vérifier que le temps actuel n'est pas égal à l'heure actuelle
    current_time_in_seconds = time.time() * 1000
    assert current_time != current_time_in_seconds