# 4 — Arbres, forêts et gradient boosting

## L’arbre de décision

Un arbre pose une suite de questions : « la largeur est-elle supérieure à 90 ? »,
« le canal alpha contient-il beaucoup de pixels transparents ? », etc. Chaque réponse
envoie l’image vers une branche jusqu’à une prédiction.

### Analogie : le jeu des vingt questions

Pour deviner un objet, on pose des questions qui séparent au mieux les possibilités. Un
arbre fait pareil avec les nombres. Il est interprétable, mais un arbre unique peut apprendre
par cœur des accidents du train.

## Extra Trees : faire voter une forêt

Une forêt entraîne de nombreux arbres avec de l’alêtoire dans les variables et les seuils,
puis moyenne leurs probabilités. Les erreurs individuelles ont alors une chance de s’annuler.
Notre modèle Extra Trees sur les features de style atteint environ **0,936 d’accuracy** et
**0,942 de macro-F1**.

## Gradient boosting : corriger les erreurs successivement

Le boosting ne fait pas voter des arbres indépendants. Chaque nouvel arbre cherche à
corriger une partie des erreurs du groupe déjà construit.

### Analogie : une copie corrigée en plusieurs passages

Au premier passage, on repère les erreurs grossières. Au suivant, on se concentre sur ce qui
reste faux. De petites corrections successives forment une solution forte. Le **learning
rate** limite l’importance de chaque correction pour éviter une réaction excessive.

`HistGradientBoostingClassifier` regroupe les valeurs continues dans des intervalles avant
de chercher les coupures. Cela rend l’apprentissage efficace. Sur notre validation, il atteint
environ **0,960 d’accuracy** et **0,965 de macro-F1**.

## Pourquoi il marche si bien ici

Les arbres capturent naturellement des règles non linéaires comme « grande image ET
transparence faible ET saturation moyenne ». Les dimensions, le mode PNG, la taille du
fichier et les statistiques alpha décrivent fortement le pipeline graphique du fournisseur.

Mais cette force est aussi un risque : le modèle peut apprendre le processus d’exportation
du dataset plus que le style visuel. C’est pourquoi nous conservons aussi MobileNet et testons
leur combinaison.

## Dans notre code

- `src/emoji_provider/features.py` construit les variables tabulaires.
- `src/emoji_provider/model.py` construit Extra Trees ou gradient boosting selon la configuration.
- `scripts/train_style.py` lance Extra Trees ; le boosting utilise `scripts/train.py` avec
  `configs/style_boosting.yaml`.

## À savoir expliquer

1. Quelle différence entre bagging/forêt et boosting ?
2. Pourquoi un arbre n’a-t-il pas besoin de standardisation ?
3. Quelle expérience permettrait de tester la dépendance aux métadonnées ?

## Ressources fiables

- [scikit-learn — ensembles d’arbres](https://scikit-learn.org/stable/modules/ensemble.html)
- [scikit-learn — HistGradientBoostingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html)
- [StatQuest — Gradient Boost for Classification](https://www.youtube.com/watch?v=jxuNLH5dXCs)
