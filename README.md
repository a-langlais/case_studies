## Projet : Prédiction du churn client à l'aide du Machine Learning

Ce petit side project a pour objectif de mettre en lumière un cas pratique usuel du Machine Learning dans la vie réelle. Il suit une logique classique de projet de Data Science et permet d'illustrer le raisonnement nécessaire à ce type de projet.
Les données utilisées sont des données fictives provenant de Kaggle.

### Quelques définitions :
- **Churn client** : Mesure du taux de clients qui arrêtent de consommer un service ou qui quittent une entreprise sur une période donnée.
- **Machine Learning** : Ensemble de techniques et d’algorithmes permettant à une machine d’apprendre à partir de données pour effectuer des prédictions ou des classifications sans être explicitement programmée pour cela.
- **Feature Engineering** : Processus de transformation et de sélection des variables (features) à partir de données brutes pour améliorer la performance des modèles de machine learning.
- **Standardisation** : Méthode de mise à l’échelle des données pour que toutes les variables aient une même échelle et évitent que certaines caractéristiques, comme les montants financiers, n'aient un poids excessif dans le modèle.
- **Régression logistique** : Modèle de machine learning utilisé pour prédire un résultat binaire (ici, churn ou non churn).
- **Précision** : Pourcentage de prédictions correctes parmi les résultats positifs prédits par le modèle (ici, les churns correctement identifiés).
- **Rappel** : Proportion de churns correctement identifiés parmi l’ensemble des churns réels.
- **F1-score** : Moyenne harmonique entre la précision et le rappel, utile dans les situations de déséquilibre des classes.

### Introduction

Le churn client est une problématique majeure pour les entreprises qui souhaitent maintenir leur clientèle et éviter les départs massifs. Ce projet vise à prédire le churn en utilisant les données clients à travers des techniques de machine learning, permettant aux entreprises d’identifier à l’avance les clients susceptibles de partir. Cela permet de déployer des actions marketing ciblées pour améliorer la fidélisation et la satisfaction client. Le fichier de données utilisé contient des informations variées sur les abonnements, les services consommés, et les profils démographiques des clients. L'objectif final est de construire un modèle capable de prédire si un client quittera l'entreprise ou non.

### Exploration des données

L'exploration des données commence par l'importation des bibliothèques Python essentielles comme `numpy`, `pandas`, `matplotlib`, `seaborn`, et `sklearn`. Ensuite, les données clients, issues du fichier `churn.csv` (disponible dans le répertoire `\data`), sont chargées. Ce fichier contient 7043 lignes et 21 colonnes, dont des informations telles que le genre, le type de contrat, les services utilisés (Internet, télévision, etc.), ainsi que des données financières (charges mensuelles, paiements).

L'analyse préliminaire permet d'examiner la distribution des variables et de vérifier les valeurs manquantes. Par exemple, la fonction `df.isna().sum()` est utilisée pour vérifier si certaines colonnes ont des valeurs manquantes qui pourraient compromettre la qualité du modèle. Ensuite, une analyse exploratoire des données (EDA) est menée à l'aide de visualisations pour identifier les tendances et les corrélations possibles entre le churn et les autres variables. Par exemple, un graphique `sns.countplot()` peut montrer que 26,54 % des clients ont quitté l’entreprise, et d'autres visualisations permettent de comparer le churn en fonction du genre ou des services utilisés.

### Data cleaning & Data processing

La préparation des données est une étape essentielle avant l’entraînement du modèle. Elle consiste d'abord à nettoyer les données en supprimant les colonnes non pertinentes comme `customerID`, qui n’a pas d’impact direct sur la probabilité de churn. Ensuite, les variables catégorielles (comme le genre, le type de contrat, etc.) sont transformées en valeurs numériques à l'aide du `LabelEncoder` pour qu'elles soient compatibles avec les algorithmes de machine learning.

Une autre étape importante est la standardisation des variables numériques comme les charges mensuelles (`MonthlyCharges`) et les durées d'abonnement (`tenure`). Cette standardisation permet de s'assurer que toutes les variables sont sur la même échelle afin qu'aucune ne domine les autres lors de l'entraînement du modèle.

Les données sont ensuite divisées en deux sous-ensembles : 80 % pour l'entraînement et 20 % pour le test à l'aide de la fonction `train_test_split`. Cela permet de construire le modèle sur une partie des données et de l’évaluer sur l'autre partie pour obtenir une mesure réaliste de ses performances.

### Construction du modèle prédictif

Pour prédire le churn, nous utilisons une régression logistique, un algorithme de classification binaire adapté pour ce type de problème où l'objectif est de prédire deux résultats possibles : churn ou non churn. La régression logistique est un modèle simple mais puissant, souvent utilisé lorsque l'on travaille avec des variables cibles binaires. L'entraînement du modèle est effectué sur les données d'entraînement (`X_train` et `y_train`) avec la méthode `model.fit()`, et le modèle est ensuite testé sur les données de test (`X_test`).

Ce modèle produit des probabilités qui sont ensuite converties en prédictions binaires : 1 pour churn et 0 pour non churn. Le choix d'une régression logistique permet également de comprendre l'impact relatif de chaque variable sur la probabilité de churn, grâce aux coefficients du modèle.

### Evaluation des performances

L’évaluation du modèle se fait à travers des métriques de classification telles que la précision, le rappel et le f1-score. Ces mesures sont obtenues grâce à la fonction `classification_report()`. La précision indique le pourcentage de churns correctement prédits parmi tous les churns prédits, tandis que le rappel indique combien de churns réels le modèle a réussi à identifier. Le f1-score offre une mesure équilibrée en tenant compte à la fois de la précision et du rappel, ce qui est crucial dans des cas comme le churn où les données sont souvent déséquilibrées (peu de clients quittent par rapport à ceux qui restent).

Dans ce projet, le modèle atteint une précision de 82 %, ce qui est un bon indicateur de performance pour un modèle de churn. Cependant, le rappel est légèrement plus bas, ce qui suggère que le modèle pourrait manquer certains clients churners. Ces résultats fournissent des informations précieuses pour ajuster les stratégies commerciales et améliorer le modèle si nécessaire.

### Interpretation et conclusion

Le modèle prédictif développé dans ce projet a des implications significatives pour les entreprises qui cherchent à réduire leur taux de churn. En identifiant les clients les plus susceptibles de partir, les équipes marketing et les départements de relation client peuvent déployer des campagnes ciblées pour retenir ces clients. Par exemple, un client identifié comme à risque pourrait se voir offrir une promotion ou bénéficier d’un support technique amélioré. Cela permet non seulement de réduire les pertes, mais aussi de maximiser la fidélité et la satisfaction client, augmentant ainsi la rentabilité à long terme.

En conclusion, la prédiction du churn via le machine learning permet aux entreprises de prendre des décisions éclairées et d’agir de manière proactive pour minimiser les départs de clients. Le modèle basé sur la régression logistique utilisé dans ce projet offre une solution simple mais efficace, intégrable dans les systèmes CRM pour soutenir les stratégies de rétention client.