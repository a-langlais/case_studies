## Ensemble d'études de cas

Ce repo personnel à pour objectif de classer différents petits projets d'étude de cas plus-ou-moins développés, visant à mettre en application des notions de data science et développer des concepts et des problématiques métiers pour contribuer à ma culture générale et ma veille technologique.
Chaque subrepo concerne une étude de cas avec toujours à minima une petite présentation, le jeu de données utilisé et sa source, les scripts/notebooks créés et les outputs.

### 🧬 Séquençage d'ADN à l'aide du Machine Learning

En génomique, le traitement des séquences d'ADN comme un langage est appelé "comptage de k-mers", cela consiste à compter les occurences de chaque k-mer possible. Bien qu'il existe des outils spécialisés en bioinformatique pour cette tâche, les outils de traitement du langage naturel (NLP) en Python facilitent beaucoup ce processus. On peut voir l'ADN comme le langage de programmation des êtres vivants, qui encode des instructions et des fonctions pour les molécules présentes dans toutes les formes de vie.
La longueur des mots et la quantité de chevauchement doivent être déterminées empiriquement mais le Machine Learning peut justement permettre d'apporter une aide considérable dans la compréhension de ce langage et dans la prédiction des chaines pour des contextes données.
Trois fichiers de données sont utilisés comprenant des séquences d'ADN humains, de chimpanzés et de chiens.

Ainsi, les séquences d'ADN sont traitées comme un langage en utilisant des mots de longueur fixe, ici des héxamères (k = 6), choisis arbitrairement. Pour ce faire, une fonction `getKmers()` permet de sélectionner la taille (par défaut k = 6 donc) et de retourner une liste de la séquence. Les k-mers ainsi récupérés sont ensuite convertis en texte à l'aide d'un `CountVectorizer` pour être par la suite transformés en séquences de vecteurs caractéristiques permettant d'appliquer un modèle "Bag of Words".
Les ensembles d'entrainement et de test ont été utilisés pour entrainer un classificateur Naive Bayes multinomial `MultinomialNB` puis les performances du modèles sont évalués en utilisant des métriques telles que la matrice de confusion, l'exactitude, la précision, le rappel et le F1-Score.
Les résultats montrent une excellente performance du modèle sur les données de test, indiquant que le modèle ne surajuste pas les données d'entrainement.

Cette étude de cas est intéressante car elle permet de mettre en application la décomposition d'une chaine de caractères en vecteurs de longueur uniforme pour une utilisation dans des algorithmes de classification ou de régression.

### 🔮 Prédiction des assurances

### ❌ Prédiciton du churn client

Le churn client est une problématique majeure pour les entreprises qui souhaitent maintenir leur clientèle et éviter les départs massifs. Ce projet vise à prédire le churn en utilisant les données clients à travers des techniques de machine learning, permettant aux entreprises d’identifier à l’avance les clients susceptibles de partir.
Le fichier de données utilisé contient des informations variées sur les abonnements, les services consommés, et les profils démographiques des clients. L'objectif final est de construire un modèle capable de prédire si un client quittera l'entreprise ou non.

Après une phase exploration du jeu de données et une vérification de la qualité et de l'intégrité des données, une phase de préprocessing est indispensable pour pouvoir utiliser certains algorithmes de Machine Learning. Dans un premier temps, un `LabelENcoder` est utilisé afin de trnasformer les variables catégorielles en variables numériques. Par la suite, les variables numériques quantitatives sont standardisées pour unformiser le poids explicatifs dans les futurs modèles.
Les ensembles d'entrainement et de test ont été utilisés pour entrainer quatre modèles différents dans un premier temps : une régression logistique (`LinearRegression`), un classifieur des K plus proches voisins (`KNeighborsClassifier`), un Support Vector Machine `SVC` et un modèle de forêt aléatoire (`RandomForestClassifier`).
Le modèle avec la meilleure performance a été conservé, il s'agit de la régression logistique, particulièrement adaptée à ce genre de problématique binaire (départ/non départ). Ainsi, ce modèle a été optimisé via une recherche fine des meilleurs hyperparamètres à l'aide d'une `GridSearchCV`.
Les résultats montrent une précision d'environ 82%, ce qui est un bon indicateur de performance pour un modèle sur ce type de problématique métier.

Cette étude de cas permet de suivre une ligne rouge classique en data tout en mettant en lumière la comparaison de plusieurs modèles face à une problématique métier, montrant que plusieurs solutions peuvent être possibles.

### 🪢 Théorie des graphs sur les mots-clés de StackOverflow

L'objectif de ce petit notebook est de créer une représentation visuelle d'un réseau représentant les groupes associés par les mots clés les plus utilisés sur le site StackOverflow.

Le graphique est généré en utilisant la bibliothèque `networkx` en Python, avec une disposition de type `spring_layout` qui optimise la position des nœuds pour minimiser les chevauchements et maximiser la lisibilité. Le paramètre k de cette disposition a été ajusté pour augmenter l'espace entre les nœuds, facilitant ainsi la visualisation des connexions et des groupes.

Les couleurs des nœuds sont définies par une palette prédéfinie, où chaque groupe est représenté par une couleur distincte. Les tailles des nœuds sont proportionnelles à leur `nodesize`, permettant de visualiser rapidement les nœuds les plus importants ou influents dans le réseau.

Ce graphique est un outil puissant pour analyser les relations et les structures au sein du réseau, offrant une vue d'ensemble claire et informative des interactions entre les différents éléments.

### ⏲️ Séries temporelles et prédictions