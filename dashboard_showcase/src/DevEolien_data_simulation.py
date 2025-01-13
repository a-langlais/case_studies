"""
===============================================================================
Script : DevEolien_data_simulation.py

Description :
Ce script génère un jeu de données fictif pour simuler des séries temporelles 
de température, de vitesse du vent, de rentabilité de modèles de turbines, et 
de bridage des turbines. Les données sont réalistes grâce à l'intégration de 
variations saisonnières, interannuelles, et de bruit aléatoire.

Fonctionnalités principales :
- Simulation de la température :
  - Saisonnalité annuelle (plus chaud en été, plus froid en hiver).
  - Variation jour/nuit (plus froid la nuit).
  - Intégration de variations interannuelles (canicules, hivers doux).
  - Bruit aléatoire pour ajouter du réalisme.
- Simulation de la vitesse du vent :
  - Saisonnalité avec des vents plus forts en automne/hiver.
  - Variations interannuelles pour refléter des années venteuses ou calmes.
  - Périodes prolongées de vent fort ou de calme pour un réalisme accru.
- Calcul de la rentabilité :
  - Rentabilité calculée pour trois modèles de turbines éoliennes ("EcoWind", 
    "SkyBlade", "GreenPower") en fonction de la vitesse du vent et de coefficients spécifiques.
- Simulation du bridage :
  - Détection des périodes où les turbines sont bridées en fonction de l'heure 
    et de la saison.
- Exportation des données :
  - Sauvegarde des données dans un fichier CSV prêt pour l'analyse ou la visualisation.

Utilisation :
1. Configurez la période de simulation et les paramètres dans le script (par 
   défaut, de 2015 à 2024, avec une résolution de 10 minutes).
2. Exécutez le script pour générer un fichier CSV nommé 'wind_turbine_data.csv'.

Dépendances :
- Python >= 3.7
- Bibliothèques : pandas, numpy, random

Notes :
- Les données générées sont synthétiques et ne reflètent pas des mesures 
  réelles. Elles sont destinées à des démonstrations ou à des études 
  nécessitant des données fictives.
- Le bruit aléatoire permet d’éviter des patterns trop réguliers dans les séries.

Exemple de commande pour exécuter le script :
    python wind_turbine_data_simulation.py

===============================================================================
"""

import pandas as pd
import numpy as np
import random

random.seed(42)

# Générer des facteurs de variation interannuelle pour température et vent
def generate_annual_factors(start_year, end_year):
    years = range(start_year, end_year + 1)
    temp_factors = {year: random.uniform(-2, 2) for year in years}  # Canicules, hivers doux
    wind_factors = {year: random.uniform(-1, 1) for year in years}  # Années venteuses/calmes
    return temp_factors, wind_factors

# Fonction pour simuler la température avec variations inter et intra-annuelles
def simulate_temperature(date, annual_factors):
    year = date.year
    day_of_year = date.timetuple().tm_yday
    hour = date.hour

    # Base saisonnière : temp moyenne varie entre -5 en hiver et 25 en été
    seasonal_temp = 15 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + 10

    # Variation jour/nuit : plus froid la nuit
    daily_variation = 5 * np.sin(2 * np.pi * (hour - 5) / 24)

    # Variation interannuelle (canicules, hivers doux)
    interannual_variation = annual_factors[year]

    # Bruit aléatoire
    noise = np.random.normal(0, 2)

    return round(seasonal_temp + daily_variation + interannual_variation + noise, 1)

# Fonction pour simuler la vitesse du vent avec variations et périodes continues de vent fort ou calme
def simulate_wind_speed(date, annual_factors):
    year = date.year
    day_of_year = date.timetuple().tm_yday

    # Base saisonnière : vent moyen plus élevé en automne/hiver
    seasonal_wind = 3 * np.cos(2 * np.pi * (day_of_year - 300) / 365) + 5

    # Variation interannuelle
    interannual_variation = annual_factors[year]

    # Introduire des périodes de vent fort ou calme
    persistent_variation = np.random.choice([0, 2, -2], p=[0.85, 0.1, 0.05])  # Moments avec ou sans vent prolongés

    # Bruit aléatoire
    noise = np.random.normal(0, 1.5)

    return round(max(seasonal_wind + interannual_variation + persistent_variation + noise, 0), 1)

# Générer les facteurs interannuels
start_year = 2015
end_year = 2025
temp_factors, wind_factors = generate_annual_factors(start_year, end_year)

# Fonction pour simuler la rentabilité (dépend de la vitesse du vent et du modèle)
def simulate_rent(wind_speed, model):
    base_rent = wind_speed * random.uniform(2, 35)
    model_factor = {"EcoWind": 1.187, "SkyBlade": 1.0, "GreenPower": 0.885}
    return round(base_rent * model_factor[model], 2)

# Gérer les colonnes de rentabilité pour chaque modèle
def calculate_rents_for_models(wind_speed):
    models = ["EcoWind", "SkyBlade", "GreenPower"]
    rents = {}
    for model in models:
        rents[model] = simulate_rent(wind_speed, model)
    return rents

# Fonction pour déterminer le bridage
def calculate_bridage(date):
    hour = date.hour
    month = date.month

    if 6 <= month <= 8:  # Été
        if (22 <= hour < 24) or (0 <= hour < 2):
            return 1
    elif 12 <= month or month <= 2:  # Hiver
        if 15 <= hour < 22:
            return 1
    else:  # Printemps et Automne
        if (18 <= hour < 24) or (0 <= hour < 2):
            return 1
    return 0

# Générer le jeu de données
start_date = pd.Timestamp("2015-01-01 00:00")
end_date = pd.Timestamp("2024-12-31 23:50")

# Créer un index temporel avec une ligne toutes les 10 minutes
date_range = pd.date_range(start=start_date, end=end_date, freq="10T")

data = []
for date in date_range:
    temperature = simulate_temperature(date, temp_factors)
    wind_speed = simulate_wind_speed(date, wind_factors)
    rents = calculate_rents_for_models(wind_speed)
    bridage = calculate_bridage(date)
    data.append([date, temperature, wind_speed, rents["EcoWind"], rents["SkyBlade"], rents["GreenPower"], bridage])

# Création du DataFrame
df = pd.DataFrame(data, columns=["Date", "Temperature", "WindSpeed", "Rent_EcoWind", "Rent_SkyBlade", "Rent_GreenPower", "Bridage"])

# Exporter vers un fichier CSV
df.to_csv("data/wind_turbine_data.csv", index=False)

print("Jeu de données généré avec succès et sauvegardé dans 'windturbine_data.csv'")
