# 2 — Transformer une image en caractéristiques

## Pourquoi extraire des caractéristiques ?

Donner tous les pixels bruts à un modèle classique crée des milliers de variables et ne
lui dit pas ce qui compte. Une **feature** est une mesure choisie pour résumer un aspect de
l’image : couleur dominante, saturation, orientation des contours ou quantité de transparence.

### Analogie : décrire un tableau au téléphone

Tu ne peux pas envoyer le tableau. Tu annonces donc : « beaucoup de jaune, peu de bleu,
des contours arrondis et une zone transparente autour ». Tu as compressé l’image en une
fiche descriptive. Le modèle apprend à partir de ces fiches.

## Histogrammes RGB et HSV

Un histogramme compte combien de pixels appartiennent à chaque plage de valeurs. Il ignore
presque toute la position : deux images avec les mêmes couleurs peuvent avoir des dessins
différents. HSV sépare la **teinte**, la **saturation** et la **luminosité**, souvent plus
faciles à interpréter que le mélange RGB.

## HOG : Histogram of Oriented Gradients

HOG résume les directions des contours :

1. calculer le gradient horizontal et vertical ;
2. convertir ces gradients en force et orientation ;
3. compter les orientations dans de petites cellules ;
4. normaliser les cellules par blocs pour réduire l’effet de l’éclairage.

### Analogie : les coups de crayon

Au lieu de retenir la couleur d’un portrait, HOG compte les coups de crayon horizontaux,
verticaux et diagonaux dans chaque zone. La méthode a été popularisée par Dalal et Triggs
en 2005 pour la détection de piétons, avant la domination des CNN.

## Ce que notre expérience montre

Notre modèle HOG + couleur atteint environ **0,757 d’accuracy** et **0,749 de macro-F1**.
Il reconnaît des styles, mais perd des détails fins et des informations de fichier. Un score
plus faible n’en fait pas une mauvaise expérience : il permet d’identifier ce qui manque.

## Dans notre code

- `src/emoji_provider/features.py` calcule les descripteurs visuels.
- `scripts/train_hog.py` entraîne et sauvegarde le pipeline.
- `scripts/predict.py` crée la soumission en chargeant le modèle HOG sauvegardé.

## À savoir expliquer

1. Quelle information spatiale un histogramme de couleurs perd-il ?
2. Pourquoi HOG résiste-t-il mieux à une variation de luminosité que les pixels bruts ?
3. Pourquoi standardiser les features avant un modèle linéaire ?

## Ressources fiables

- [scikit-image — explication et exemple officiel de HOG](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html)
- [Article historique de Dalal et Triggs](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)
