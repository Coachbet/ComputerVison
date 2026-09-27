# 3 — Régression logistique et validation

## Un classifieur linéaire

Malgré son nom, la régression logistique sert ici à **classifier**. Pour chaque fournisseur,
elle calcule un score à partir d’une somme pondérée des features. La fonction softmax
transforme ensuite les scores en probabilités dont la somme vaut 1.

`score_classe = biais + w1×feature1 + w2×feature2 + ...`

### Analogie : un jury avec une grille de points

Chaque indice donne ou retire des points aux candidats. Beaucoup de jaune peut favoriser
un fournisseur, un certain type de contour un autre. Le candidat avec le total le plus haut
gagne. L’apprentissage consiste à trouver les poids de la grille.

## Pourquoi standardiser ?

Si une feature varie entre 0 et 1 et une autre entre 0 et 100 000, leur échelle fausse
l’optimisation et la régularisation. `StandardScaler` centre et réduit chaque colonne. Il doit
être ajusté uniquement sur le train, d’où l’utilisation d’un `Pipeline` scikit-learn.

## Une validation honnête

Nous gardons une partie des images avec leurs labels hors de l’entraînement. La séparation
est **stratifiée** afin de conserver la proportion de chaque fournisseur. Tous les modèles
sont comparés sur la même séparation et la même graine aléatoire.

- **Accuracy** : proportion totale de bonnes prédictions.
- **F1 d’une classe** : compromis entre précision et rappel.
- **Macro-F1** : moyenne des F1 de toutes les classes, avec le même poids pour chaque classe.

Notre baseline couleur obtient environ **0,780 d’accuracy** et **0,797 de macro-F1**. Une
fois le choix du modèle terminé, on peut le réentraîner sur toutes les données labellisées.

## Dans notre code

- `src/emoji_provider/training.py` crée la séparation et calcule les métriques.
- `scripts/train.py` entraîne la baseline.
- `outputs/metrics/` conserve les résultats au lieu de se fier à la mémoire.

## Piège majeur : la fuite de données

Calculer le scaler sur train + validation, choisir sans cesse selon la même validation ou
mettre deux variantes du même fichier des deux côtés donne un score trop optimiste.

## À savoir expliquer

1. Pourquoi le nom « régression logistique » est-il trompeur ici ?
2. Que mesure la macro-F1 que l’accuracy peut masquer ?
3. Pourquoi Kaggle ne remplace-t-il pas une validation locale ?

## Ressources fiables

- [scikit-learn — régression logistique](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [scikit-learn — métriques de classification](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [3Blue1Brown — gradient descent](https://www.youtube.com/watch?v=IHZwWFHWa-w)
