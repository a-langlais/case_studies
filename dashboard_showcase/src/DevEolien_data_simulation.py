import pandas as pd
import numpy as np
import random

# Fonction pour simuler la température
# Plus froid en hiver, plus chaud en été, variation jour/nuit
def simulate_temperature(date):
    day_of_year = date.timetuple().tm_yday
    hour = date.hour
    
    # Base saisonnière : temp moyenne varie entre -5 en hiver et 25 en été
    seasonal_temp = 15 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + 10
    
    # Variation jour/nuit : plus froid la nuit
    daily_variation = 5 * np.sin(2 * np.pi * (hour - 5) / 24)

    # Ajouter un bruit aléatoire
    noise = np.random.normal(0, 2)

    return round(seasonal_temp + daily_variation + noise, 1)

# Fonction pour simuler la vitesse du vent (plus élevée en automne/hiver)
def simulate_wind_speed(date):
    day_of_year = date.timetuple().tm_yday

    # Base saisonnière : vent moyen plus élevé en automne/hiver
    seasonal_wind = 3 * np.cos(2 * np.pi * (day_of_year - 300) / 365) + 5

    # Ajouter un bruit aléatoire
    noise = np.random.normal(0, 1.5)

    return round(max(seasonal_wind + noise, 0), 1)

# Fonction pour simuler la rentabilité (dépend de la vitesse du vent et du modèle)
def simulate_rent(wind_speed, model):
    base_rent = wind_speed * random.uniform(5, 15)
    model_factor = {"Model A": 1.1, "Model B": 1.0, "Model C": 0.9}
    return round(base_rent * model_factor[model], 2)

# Gérer les colonnes de rentabilité pour chaque modèle
def calculate_rents_for_models(wind_speed):
    models = ["Model A", "Model B", "Model C"]
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
    temperature = simulate_temperature(date)
    wind_speed = simulate_wind_speed(date)
    rents = calculate_rents_for_models(wind_speed)
    bridage = calculate_bridage(date)
    data.append([date, temperature, wind_speed, rents["Model A"], rents["Model B"], rents["Model C"], bridage])

# Création du DataFrame
df = pd.DataFrame(data, columns=["Date", "Temperature", "WindSpeed", "Rent_Model_A", "Rent_Model_B", "Rent_Model_C", "Bridage"])

# Exporter vers un fichier CSV
df.to_csv("data/wind_turbine_data.csv", index=False)

print("Jeu de données généré avec succès et sauvegardé dans 'wind_turbine_data.csv'")
