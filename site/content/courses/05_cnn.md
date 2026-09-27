# 5 — CNN, convolution et LeNet

## Pourquoi un CNN ?

Un réseau dense traiterait le pixel en haut à gauche comme une variable sans rapport avec
son voisin. Un **Convolutional Neural Network** exploite au contraire la proximité spatiale et
réutilise le même petit filtre partout dans l’image.

### Analogie : une loupe qui glisse

Imagine une petite loupe qui parcourt l’image. Une loupe apprend à réagir aux bords verticaux,
une autre aux courbes ou aux contrastes. Dans les couches suivantes, ces indices simples se
combinent en formes, puis en motifs de style plus complexes.

## Les briques du réseau

- **Convolution (`Conv2D`)** : applique des filtres appris dans chaque zone locale.
- **ReLU** : remplace les valeurs négatives par zéro et introduit de la non-linéarité.
- **Pooling** : réduit la résolution en gardant l’information la plus forte.
- **Dense + softmax** : combine les motifs et produit les probabilités des classes.
- **Dropout** : masque aléatoirement des activations pendant l’entraînement pour limiter
  l’apprentissage par cœur.

## Un peu d’histoire

LeNet-5, publié par Yann LeCun et ses coauteurs en 1998, a popularisé les convolutions pour
la lecture de chiffres manuscrits. AlexNet a relancé les CNN profonds en gagnant ImageNet en
2012 grâce notamment aux GPU, à ReLU et au dropout.

## Notre LeNet et ce que son score enseigne

Notre petit CNN atteint environ **0,426 d’accuracy** et **0,426 de macro-F1**. Ce résultat est
nettement inférieur à la baseline. Les raisons plausibles sont la quantité de données, un
entraînement court, le redimensionnement et la difficulté d’apprendre de zéro des signatures
de style parfois subtiles.

Un résultat négatif est scientifiquement utile s’il est comparé proprement et expliqué. Il
motive naturellement l’expérience suivante : partir d’un réseau déjà entraîné.

## Dans notre code

- `src/emoji_provider/cnn.py` définit le réseau et le chargement des images.
- `scripts/train_cnn.py` entraîne avec augmentation, pondération et early stopping.
- `scripts/predict_cnn.py` génère le CSV associé.

## À savoir expliquer

1. Pourquoi partage-t-on le même filtre à toutes les positions ?
2. Que perd et que gagne le pooling ?
3. Pourquoi le score de validation peut-il se dégrader alors que le train continue de monter ?

## Ressources fiables

- [TensorFlow — tutoriel CNN officiel](https://www.tensorflow.org/tutorials/images/cnn)
- [StatQuest — Neural Networks Part 8: Image Classification with CNNs](https://www.youtube.com/watch?v=HGwBXDKFk9I)
- [Article LeNet-5](http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf)
