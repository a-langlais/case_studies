import pandas as pd
import random
from faker import Faker

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

# Liste des situations familiales
situations_familiales = ["Célibataire", "Marié", "Divorcé", "Veuf", "Concubinage"]

# Liste des statuts professionnels
statuts_professionnels = ["Actif", "Chômeur", "Retraité", "Étudiant"]

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
probabilites_revenus = {
    "Très faible": 0.10,
    "Faible": 0.40,
    "Moyen": 0.40,
    "Élevé": 0.08,
    "Très élevé": 0.02,
}

# Catégories sociales basées sur le niveau de revenu
def assigner_categorie_sociale(niveau_revenu, statut_professionnel):
    if niveau_revenu == "Très faible":
        if statut_professionnel in ["Chômeur", "Retraité"]:
            return "Catégorie 4 (Chômeur/Retraité)"
        return "Catégorie 3 (Ouvrier)"
    elif niveau_revenu == "Faible":
        return "Catégorie 3 (Ouvrier)"
    elif niveau_revenu == "Moyen":
        return "Catégorie 2 (Employé/Technicien)"
    elif niveau_revenu == "Élevé":
        return "Catégorie 1 (Cadre)"
    else:
        return "Catégorie 1 (Cadre)"

# Liste des niveaux d'études et leurs probabilités de revenus associés pour plus de réalisme
niveaux_etudes = ["Sans diplôme", "Brevet", "Baccalauréat", "BTS/DUT", "Licence", "Master", "Doctorat"]

def ajuster_probabilites_revenus_par_etudes(niveau_etudes):
    if niveau_etudes == "Sans diplôme":
        return {
            "Très faible": 0.40,
            "Faible": 0.45,
            "Moyen": 0.10,
            "Élevé": 0.04,
            "Très élevé": 0.01,
        }
    elif niveau_etudes == "Brevet":
        return {
            "Très faible": 0.30,
            "Faible": 0.50,
            "Moyen": 0.15,
            "Élevé": 0.04,
            "Très élevé": 0.01,
        }
    elif niveau_etudes == "Baccalauréat":
        return {
            "Très faible": 0.20,
            "Faible": 0.40,
            "Moyen": 0.30,
            "Élevé": 0.08,
            "Très élevé": 0.02,
        }
    elif niveau_etudes == "BTS/DUT":
        return {
            "Très faible": 0.10,
            "Faible": 0.30,
            "Moyen": 0.40,
            "Élevé": 0.15,
            "Très élevé": 0.05,
        }
    elif niveau_etudes == "Licence":
        return {
            "Très faible": 0.05,
            "Faible": 0.20,
            "Moyen": 0.40,
            "Élevé": 0.30,
            "Très élevé": 0.05,
        }
    elif niveau_etudes == "Master":
        return {
            "Très faible": 0.02,
            "Faible": 0.10,
            "Moyen": 0.30,
            "Élevé": 0.45,
            "Très élevé": 0.13,
        }
    else:  # Doctorat
        return {
            "Très faible": 0.01,
            "Faible": 0.25,
            "Moyen": 0.40,
            "Élevé": 0.30,
            "Très élevé": 0.04,
        }

# Fonction pour générer une composition familiale
def generer_composition_familiale():
    enfants = random.randint(0, 5)  # Nombre d'enfants (0 à 5)
    adultes = random.randint(1, 2)  # Nombre d'adultes (1 ou 2)
    return {
        "adultes": adultes,
        "enfants": enfants,
        "total": adultes + enfants,
    }

# Création des données
donnees = []
for _ in range(N):
    composition = generer_composition_familiale()
    region = random.choice(list(regions_departements.keys()))
    departement = random.choice(regions_departements[region])

    # Attribution du niveau d'études
    niveau_etudes = random.choice(niveaux_etudes)
    
    # Ajuster les probabilités de revenus en fonction du niveau d'études
    probabilites_revenus_etudes = ajuster_probabilites_revenus_par_etudes(niveau_etudes)

    # Attribution du niveau de revenu en fonction des probabilités ajustées
    niveau_revenus = random.choices(
        list(probabilites_revenus_etudes.keys()), 
        weights=list(probabilites_revenus_etudes.values()), 
        k=1
    )[0]
    
    # Initialiser les allocations à 0 pour chaque allocataire
    allocations_attribuees = {allocation: 0 for allocation in allocations}

    # Pour les autres (revenus très faibles, faibles et moyens), attribuer potentiellement des allocations
    for allocation, prob in allocations.items():
        if random.random() < prob:
            if allocation == "Allocation parent isolé (API)" and composition["adultes"] != 1: # Seulement pour les familles monoparentales
                continue
            if allocation == "Allocation familiale (AF)" and composition["enfants"] < 2: # Seulement pour les familles avec au moins 2 enfants
                continue
            if allocation in ["Revenu de solidarité active (RSA)", "Aide personnalisée au logement (APL)"] and niveau_revenus in ["Élevé", "Très élevé"]:
                continue
            allocations_attribuees[allocation] = 1

    statut_professionnel = random.choice(statuts_professionnels)
    categorie_sociale = assigner_categorie_sociale(niveau_revenus, statut_professionnel)

    donnees.append(
        {
            "ID_Allocataire": faker.uuid4(),
            "Nom": faker.last_name(),
            "Prénom": faker.first_name(),
            "Date_Naissance": faker.date_of_birth(minimum_age=18, maximum_age=90),
            "Région": region,
            "Département": departement,
            "Situation_Familiale": random.choice(situations_familiales),
            "Statut_Professionnel": statut_professionnel,
            "Niveau_Etudes": niveau_etudes,
            "Niveau_Revenus": niveau_revenus,
            "Categorie_Sociale": categorie_sociale,
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
