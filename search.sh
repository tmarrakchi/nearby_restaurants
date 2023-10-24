#!/bin/bash

# Analyser les arguments passés à la commande
for arg in "$@"; do
  case "$arg" in
    latitude=*)
      latitude="${arg#*=}"
      ;;
    longitude=*)
      longitude="${arg#*=}"
      ;;
    radius=*)
      radius="${arg#*=}"
      ;;
  esac
done

# Vérifier que tous les paramètres sont définis
if [ -z "$latitude" ] || [ -z "$longitude" ] || [ -z "$radius" ]; then
  echo "Utilisation : $0 latitude=XXX longitude=YYY radius=ZZZ"
  exit 1
fi

# Afficher les valeurs extraites
echo "Latitude : $latitude"
echo "Longitude : $longitude"
echo "Rayon : $radius"

# Exemple : Exécution du script Python avec les valeurs extraites
python main.py --latitude "$latitude" --longitude "$longitude" --radius "$radius"

# Garder la fenêtre du terminal ouverte
read
