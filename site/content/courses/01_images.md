# 1 — Images, pixels et transparence

## Ce qu’il faut comprendre

Une image numérique n’est pas un dessin pour l’ordinateur : c’est un tableau de nombres.
Une image RGB de 64 × 64 pixels possède la forme `(64, 64, 3)`. Pour chaque pixel,
les trois nombres mesurent les quantités de rouge, vert et bleu. Un PNG RGBA ajoute
un quatrième canal, **alpha**, qui indique la transparence.

### Analogie : une mosaïque lumineuse

Imagine une mosaïque de petites lampes. Chaque case contient trois variateurs R, G et B.
En réglant leurs intensités, on fabrique une couleur. Le canal alpha est un rideau placé
devant la lampe : `0` la cache, `255` la laisse totalement visible.

## Pourquoi c’est important ici

Nous ne cherchons pas quel emoji est dessiné, mais **quel fournisseur l’a rendu** : Apple,
Google, Samsung, etc. Deux fournisseurs peuvent dessiner le même visage avec des formes,
des couleurs, des contours et une transparence différents. Le fichier lui-même peut aussi
porter la signature d’un pipeline de rendu : dimensions, mode couleur ou taille compressée.

Dans nos données, ces indices techniques sont très prédictifs. Cela explique pourquoi
le modèle « style + métadonnées » est meilleur que notre petit CNN. Attention : si Kaggle
transforme les fichiers différemment, cette signature peut disparaître. C’est un risque de
**changement de distribution**.

## Dans notre code

- `src/emoji_provider/data.py` charge les fichiers et les labels.
- `src/emoji_provider/features.py` mesure taille, mode, transparence et statistiques visuelles.
- `scripts/train.py` charge ces descriptions avant l’entraînement.

## Mini-expérience

Ouvre deux PNG du même emoji provenant de fournisseurs différents. Zoome fortement et
compare les contours, ombres, couleurs et pixels semi-transparents. Puis demande-toi :
quelles différences survivraient si on redimensionnait toutes les images de façon identique ?

## À savoir expliquer

1. Quelle est la différence entre RGB et RGBA ?
2. Pourquoi une métadonnée peut-elle aider sans représenter le contenu visuel ?
3. Pourquoi ce raccourci peut-il mal généraliser ?

## Pour aller plus loin

- [TensorFlow — tutoriels de vision par ordinateur](https://www.tensorflow.org/tutorials/images)
- [3Blue1Brown — But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk)
