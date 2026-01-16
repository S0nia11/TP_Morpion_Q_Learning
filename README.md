# TP Morpion – Q-learning 

Ce projet a été réalisé dans le cadre d’un TP d’apprentissage par renforcement.
Il consiste à implémenter le jeu du Morpion (Tic-Tac-Toe) ainsi qu’un agent
intelligent capable d’apprendre à jouer grâce à l’algorithme de Q-learning.

---

## Objectifs du projet

- Implémenter un environnement de jeu conforme aux règles du Morpion
- Concevoir un agent d’apprentissage par renforcement basé sur le Q-learning
- Entraîner l’agent par interaction avec l’environnement
- Évaluer les performances de l’agent à l’aide de statistiques et de graphiques
- Proposer une interface graphique interactive avec Pygame

---

##  Architecture du projet

Le projet est structuré autour de plusieurs composants clairement séparés :

- **Environnement**  
  Gère le plateau de jeu, les actions légales, l’application des coups,
  la détection de fin de partie et les récompenses.

- **Agent Q-learning**  
  Apprend une politique optimale à partir des valeurs Q(s, a) stockées
  dans une table tabulaire.

- **Entraînement**  
  Boucle d’épisodes où l’agent joue contre un adversaire aléatoire afin
  d’explorer différentes stratégies.

- **Évaluation**  
  Phase distincte où l’agent est testé sans exploration (ε = 0) afin
  de mesurer objectivement ses performances.

- **Interface graphique (Pygame)**  
  Permet d’interagir avec le jeu et d’observer le comportement de l’agent.

---

##  Apprentissage par renforcement – Q-learning

L’agent utilise l’algorithme de **Q-learning**, une méthode d’apprentissage
par renforcement basée sur l’essai-erreur.

Il apprend une fonction de valeur Q(s, a) représentant la qualité d’une
action `a` dans un état `s`. Les valeurs sont mises à jour progressivement
en fonction des récompenses reçues.

### Hyperparamètres utilisés

- **Alpha (α) = 0.1**  
  Vitesse d’apprentissage (mise à jour progressive et stable)

- **Gamma (γ) = 0.95**  
  Importance accordée aux récompenses futures

- **Epsilon (ε)**  
  - Initial : 1.0 (exploration maximale)
  - Décroissance progressive pendant l’entraînement
  - Minimum pendant l’entraînement : 0.05
  - Évaluation : ε = 0 (politique gloutonne)

---

##  Entraînement de l’agent

L’agent est entraîné sur plusieurs milliers d’épisodes.
Chaque épisode correspond à une partie complète de Morpion.

Pendant l’entraînement :
- l’agent explore et exploite grâce à une politique ε-greedy
- epsilon diminue progressivement
- l’entraînement est réalisé sans interface graphique pour plus d’efficacité

---

##  Évaluation des performances

Après l’entraînement, l’agent est évalué contre un adversaire aléatoire
sur 200 parties avec ε = 0.

Les métriques évaluées sont :
- Taux de victoire
- Taux de matchs nuls
- Taux de défaites

Les résultats sont exprimés en **pourcentages** et visualisés à l’aide
de graphiques comparatifs.

Les résultats montrent :
- une augmentation du taux de victoire avec le nombre d’épisodes
- une diminution du nombre de matchs nuls
- aucune défaite observée
- une convergence vers une stratégie quasi optimale

---

##  Interface graphique (Pygame)

Une interface graphique a été développée afin de permettre :
- **Humain vs Humain**
- **Humain vs Agent**
- **Agent vs Agent**

L’interface comprend :
- un menu interactif
- un plateau centré
- une gestion correcte des tours
- un retour au menu en fin de partie

---

##  Exécution du projet

### Notebook (entraînement et évaluation)
Ouvrir le fichier :
```bash
TP_Morpion_Q_Learning.ipynb
