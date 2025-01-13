"""
===============================================================================
Script : Allocations_data_simulation.py

Description :
Ce script génère un jeu de données fictif pour simuler des allocataires de la 
CAF (Caisse d'Allocations Familiales). Il s'appuie sur la bibliothèque Faker 
pour produire des données réalistes et inclut des probabilités personnalisées 
pour des allocations, des situations familiales, des statuts professionnels, 
et des niveaux de revenus.

Fonctionnalités principales :
- Génération de données démographiques fictives (nom, prénom, âge, région, etc.).
- Simulation de compositions familiales (nombre d'adultes, enfants).
- Attribution probabiliste des niveaux de revenus, niveaux d'études, et catégories sociales.
- Calcul cohérent des droits à diverses allocations en fonction des conditions d'éligibilité.

Utilisation :
1. Configurez les paramètres (nombre d'allocataires à générer, probabilités, etc.).
2. Exécutez le script pour générer un fichier CSV contenant les données simulées.
3. Les résultats sont sauvegardés dans le fichier 'allocataires_caf_synthetiques.csv'.

Dépendances :
- Python >= 3.7
- Bibliothèques : pandas, faker, random, datetime

Notes :
- Le script est paramétré pour générer des données uniquement pour la région 
  Île-de-France, mais il peut être étendu pour inclure d'autres régions
- Les conditions d'attribution des allocations intègrent des règles de cohérence
  basées sur l'âge, le niveau de revenu, et d'autres critères.

Exemple de commande pour exécuter le script :
    python CAF_data_simulation.py

===============================================================================
"""

import pandas as pd
import random
from faker import Faker
from datetime import datetime

# Initialisation du générateur de données fictives
faker = Faker("fr_FR")
N = 2184973  # Nombre d'allocataires fictifs à générer
random.seed(42)

# Dictionnaire des allocations et de leurs probabilités
allocations = {
    "Allocation familiale (AF)": 0.036,
    "Revenu de solidarité active (RSA)": 0.435,
    "Aide personnalisée au logement (APL)": 0.15,
    "Allocation parent isolé (API)": 0.08,
    "Prestation d'accueil du jeune enfant (PAJE)": 0.045,
    "Allocation adulte handicapé (AAH)": 0.1,
    "Aide au logement social (ALS)": 0.12,
    "Allocation de solidarité spécifique (ASS)": 0.062,
    "Aide sociale à la vieillesse (ASV)": 0.159,
    "Allocation de solidarité spécifique (ASI)": 0.015
}

# Liste des statuts professionnels et leurs probabilités
statuts_professionnels = {
    "Actif": 0.424,
    "Chômeur": 0.214,
    "Retraité": 0.170,
    "Étudiant": 0.192
}

# Liste des situations familiales et leurs probabilités
situations_familiales = {
    "Célibataire": 0.267,
    "Marié": 0.401,
    "Divorcé": 0.110,
    "Veuf": 0.087,
    "Concubinage": 0.135
}

# Dictionnaire des régions et de leurs départements
# Ici, on conserve que l'Ile-de-France pour limiter le nombre de données
regions_departements = {
    # "Auvergne-Rhône-Alpes": ["Ain", "Allier", "Ardèche", "Cantal", "Drôme", "Isère", "Loire", "Haute-Loire", "Puy-de-Dôme", "Rhône", "Savoie", "Haute-Savoie"],
    # "Bourgogne-Franche-Comté": ["Côte-d'Or", "Doubs", "Jura", "Nièvre", "Haute-Saône", "Saône-et-Loire", "Yonne", "Territoire de Belfort"],
    # "Bretagne": ["Côtes-d'Armor", "Finistère", "Ille-et-Vilaine", "Morbihan"],
    # "Centre-Val de Loire": ["Cher", "Eure-et-Loir", "Indre", "Indre-et-Loire", "Loir-et-Cher", "Loiret"],
    # "Corse": ["Corse-du-Sud", "Haute-Corse"],
    # "Grand Est": ["Ardennes", "Aube", "Marne", "Haute-Marne", "Meurthe-et-Moselle", "Meuse", "Moselle", "Bas-Rhin", "Haut-Rhin", "Vosges"],
    # "Hauts-de-France": ["Aisne", "Nord", "Oise", "Pas-de-Calais", "Somme"],
    "Ile-de-France": ["Paris", "Seine-et-Marne", "Yvelines", "Essonne", "Hauts-de-Seine", "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise"],
    # "Normandie": ["Calvados", "Eure", "Manche", "Orne", "Seine-Maritime"],
    # "Nouvelle-Aquitaine": ["Charente", "Charente-Maritime", "Corrèze", "Creuse", "Dordogne", "Gironde", "Landes", "Lot-et-Garonne", "Pyrénées-Atlantiques", "Deux-Sèvres", "Vienne", "Haute-Vienne"],
    # "Occitanie": ["Ariège", "Aude", "Aveyron", "Gard", "Haute-Garonne", "Gers", "Hérault", "Lot", "Lozère", "Hautes-Pyrénées", "Pyrénées-Orientales", "Tarn", "Tarn-et-Garonne"],
    # "Pays de la Loire": ["Loire-Atlantique", "Maine-et-Loire", "Mayenne", "Sarthe", "Vendée"],
    # "Provence-Alpes-Côte d'Azur": ["Alpes-de-Haute-Provence", "Hautes-Alpes", "Alpes-Maritimes", "Bouches-du-Rhône", "Var", "Vaucluse"],
    # "Guadeloupe": ["Guadeloupe"],
    # "Martinique": ["Martinique"],
    # "Guyane": ["Guyane"],
    # "Réunion": ["Réunion"],
    # "Mayotte": ["Mayotte"],
}

# Probabilités d'attribution des niveaux de revenus (distribution réaliste)
niveaux_revenus = ["Très faible", "Faible", "Moyen", "Élevé", "Très élevé"]

# Fonction pour générer une composition familiale
def generer_composition_familiale():
    enfants = random.randint(0, 5)  # Nombre d'enfants (0 à 5)
    adultes = random.randint(1, 2)  # Nombre d'adultes (1 ou 2)
    return {
        "adultes": adultes,
        "enfants": enfants,
        "total": adultes + enfants,
    }

# Règles de cohérence entre la date de naissance, le statut professionnel et la situation familiale
def determiner_statut_et_situation(date_naissance):
    age = (pd.Timestamp.now() - pd.Timestamp(date_naissance)).days // 365
    if age < 25:
        statut = "Étudiant" if random.random() < 0.7 else random.choices(
            list(statuts_professionnels.keys()), weights=list(statuts_professionnels.values()), k=1
        )[0]
        situation = "Célibataire" if random.random() < 0.8 else random.choices(
            list(situations_familiales.keys()), weights=list(situations_familiales.values()), k=1
        )[0]
    elif age < 65:
        statut = random.choices(
            list(statuts_professionnels.keys()), weights=list(statuts_professionnels.values()), k=1
        )[0]
        situation = random.choices(
            list(situations_familiales.keys()), weights=list(situations_familiales.values()), k=1
        )[0]
    else:
        statut = "Retraité"
        situation = "Veuf" if random.random() < 0.3 else "Marié"
    return statut, situation

# Création des données
donnees = []
for _ in range(N):
    composition = generer_composition_familiale()
    region = random.choice(list(regions_departements.keys()))
    departement = random.choice(regions_departements[region])

    # Générer une date de naissance et déterminer statut professionnel et situation familiale
    date_naissance = faker.date_of_birth(minimum_age=18, maximum_age=90)
    age = (datetime.now().date() - date_naissance).days // 365
    statut_professionnel, situation_familiale = determiner_statut_et_situation(date_naissance)

    # Attribution du niveau d'études
    niveau_etudes = random.choice([
        "Sans diplôme", "Brevet", "Baccalauréat", "BTS/DUT", "Licence", "Master", "Doctorat"
    ])
    
    # Ajuster les probabilités de revenus en fonction du niveau d'études
    def ajuster_probabilites_revenus_par_etudes(niveau_etudes):
        etudes_revenus = {
            "Sans diplôme": {"Très faible": 0.4, "Faible": 0.45, "Moyen": 0.1, "Élevé": 0.04, "Très élevé": 0.01},
            "Brevet": {"Très faible": 0.3, "Faible": 0.5, "Moyen": 0.15, "Élevé": 0.04, "Très élevé": 0.01},
            "Baccalauréat": {"Très faible": 0.2, "Faible": 0.4, "Moyen": 0.3, "Élevé": 0.08, "Très élevé": 0.02},
            "BTS/DUT": {"Très faible": 0.1, "Faible": 0.3, "Moyen": 0.4, "Élevé": 0.15, "Très élevé": 0.05},
            "Licence": {"Très faible": 0.05, "Faible": 0.2, "Moyen": 0.4, "Élevé": 0.3, "Très élevé": 0.05},
            "Master": {"Très faible": 0.02, "Faible": 0.1, "Moyen": 0.3, "Élevé": 0.45, "Très élevé": 0.13},
            "Doctorat": {"Très faible": 0.01, "Faible": 0.05, "Moyen": 0.25, "Élevé": 0.6, "Très élevé": 0.09}
        }
        return etudes_revenus.get(niveau_etudes)

    probabilites_revenus_etudes = ajuster_probabilites_revenus_par_etudes(niveau_etudes)
    niveau_revenus = random.choices(
        list(probabilites_revenus_etudes.keys()),
        weights=list(probabilites_revenus_etudes.values()),
        k=1
    )[0]

    # Initialiser les allocations à 0 pour chaque allocataire
    allocations_attribuees = {allocation: 0 for allocation in allocations}

    # Attribution des allocations avec conditions
    for allocation, prob in allocations.items():
        if random.random() < prob:
            if allocation == "Allocation parent isolé (API)" and composition["adultes"] != 1:
                continue
            if allocation == "Allocation familiale (AF)" and composition["enfants"] < 2:
                continue
            if allocation in ["Revenu de solidarité active (RSA)", "Aide personnalisée au logement (APL)"] and niveau_revenus in ["Élevé", "Très élevé"]:
                continue
            if allocation == "Revenu de solidarité active (RSA)" and statut_professionnel in ["Retraité", "Étudiant"]:
                continue
            if allocation == "Allocation de solidarité spécifique (ASS)" and age < 50:
                continue
            if allocation == "Aide sociale à la vieillesse (ASV)" and age < 60:
                continue
            if allocation == "Prestation d'accueil du jeune enfant (PAJE)" and (composition["enfants"] == 0 or age > 40):
                continue
            if allocation == "Allocation adulte handicapé (AAH)" and not (18 <= age <= 59):
                continue
            if allocation == "Aide au logement social (ALS)" and niveau_revenus not in ["Très faible", "Faible"]:
                continue
            if allocation == "Allocation de solidarité spécifique (ASI)" and niveau_revenus != "Très faible":
                continue
            allocations_attribuees[allocation] = 1

    donnees.append(
        {
            "ID_Allocataire": faker.uuid4(),
            "Nom": faker.last_name(),
            "Prénom": faker.first_name(),
            "Date_Naissance": date_naissance,
            "Age": age,
            "Région": region,
            "Département": departement,
            "Situation_Familiale": situation_familiale,
            "Statut_Professionnel": statut_professionnel,
            "Niveau_Etudes": niveau_etudes,
            "Niveau_Revenus": niveau_revenus,
            "Nombre_Adultes": composition["adultes"],
            "Nombre_Enfants": composition["enfants"],
            "Nombre_Total": composition["total"],
            **allocations_attribuees,
        }
    )

# Conversion en DataFrame
df = pd.DataFrame(donnees)

# Exporter vers un fichier CSV
df.to_csv("data/allocataires_caf_synthetiques.csv", index=False, sep=";", encoding="utf-8-sig")

print("Jeu de données généré avec succès et sauvegardé dans 'allocataires_caf_synthetiques.csv'")
