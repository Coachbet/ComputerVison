# 7 — Ensemble et soumission finale

## Combiner deux points de vue

Le meilleur modèle tabulaire voit très bien la signature technique du fichier. MobileNet voit
les formes et textures. Au lieu de choisir aveuglément l’un des deux, nous moyennons leurs
probabilités :

`P_finale = 0,50 × P_style + 0,50 × P_MobileNet`

La classe de probabilité maximale devient la prédiction.

### Analogie : deux experts

Un restaurateur d’art reconnaît les traits et pigments ; un archiviste reconnaît le papier,
le format et le procédé d’impression. L’archiviste est globalement meilleur, mais le restaurateur
peut le corriger sur certains cas. Leur accord pondéré est plus robuste.

## Comment choisir le poids

On teste quelques poids sur la validation commune, sans regarder les labels du test Kaggle.
Le poids 50/50 obtient environ **0,963 d’accuracy** et **0,967 de macro-F1**, notre meilleur
résultat local. Il modifie 58 prédictions du test par rapport au boosting seul.

Il faut résister à la tentation de tester des dizaines de poids sur la même validation : on
finirait par sur-apprendre cette validation. Une validation croisée ou des prédictions
out-of-fold seraient l’étape suivante pour une estimation plus solide.

## Du modèle au CSV Kaggle

1. charger les images de test dans le même ordre que `sample_submission.csv` ;
2. calculer une probabilité pour chacune des sept classes ;
3. convertir l’indice gagnant vers le vrai label texte ;
4. conserver exactement les colonnes `Id,Label` ;
5. vérifier le nombre de lignes, les identifiants uniques et l’absence de valeurs manquantes.

Le fichier recommandé est `outputs/submissions/best_ensemble.csv`. Le boosting seul,
`best_style_boosting.csv`, reste un candidat utile : le classement Kaggle est la seule façon
de savoir lequel généralise le mieux au test caché.

## Dans notre code

- `scripts/predict_ensemble.py` aligne les classes et combine les probabilités.
- `experiments/results.csv` conserve les scores comparables.
- La page **Expériences** du site présente le classement et les limites.

## Ce qu’il faut dire dans le rapport

Expliquez l’hypothèse, le protocole, le résultat et la limite de chaque expérience. Ne dites
pas seulement « le score est meilleur ». Le recours aux métadonnées et à l’IA doit être
transparent. Reformulez avec vos propres mots après avoir compris et exécuté le code.

## À savoir expliquer

1. Pourquoi moyenne-t-on des probabilités plutôt que des labels ?
2. Dans quel cas l’ensemble serait-il moins bon que son meilleur membre ?
3. Pourquoi un score Kaggle unique ne suffit-il pas à prouver la robustesse ?

## Ressources fiables

- [scikit-learn — VotingClassifier et soft voting](https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier)
- [Kaggle Learn — cours pratiques](https://www.kaggle.com/learn)
- [StatQuest — index des vidéos de machine learning](https://statquest.org/video_index.html)
