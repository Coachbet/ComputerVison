# 6 — Transfer learning et MobileNetV3

## Ne pas repartir de zéro

Un réseau entraîné sur une grande collection d’images a déjà appris des filtres utiles :
bords, textures, courbes et compositions. Le **transfer learning** réutilise ce socle pour
une nouvelle tâche, puis apprend une petite tête de classification adaptée aux fournisseurs.

### Analogie : recruter un photographe expérimenté

On ne lui réapprend pas ce qu’est un contour ou une texture. On lui enseigne seulement les
codes graphiques d’Apple, Google ou Samsung. Avec peu de données, c’est beaucoup plus efficace
que de former un débutant complet.

## Deux phases classiques

1. **Feature extraction** : geler le backbone pré-entraîné et entraîner seulement la nouvelle
   tête. Les connaissances générales restent stables.
2. **Fine-tuning** : dégeler quelques couches hautes avec un très petit learning rate. Le
   réseau ajuste ses motifs au domaine des emojis sans oublier brutalement ce qu’il savait.

## Pourquoi MobileNetV3 ?

MobileNet est conçu pour être léger. Ses convolutions séparables traitent d’abord chaque canal
spatialement, puis les recombinent avec une convolution 1×1. Cela réduit fortement le nombre
de calculs par rapport à une convolution classique.

Notre MobileNetV3 obtient environ **0,658 d’accuracy** et **0,640 de macro-F1**. Il est moins
fort que les features de fichier, mais il apporte un point de vue réellement visuel et commet
des erreurs différentes : c’est précisément ce qui le rend utile dans l’ensemble final.

## Data augmentation

Petites rotations, translations ou zooms produisent des variantes plausibles pendant
l’entraînement. Elles jouent le rôle d’exercices supplémentaires. Une transformation trop forte
peut toutefois modifier le style recherché et nuire au modèle.

## Dans notre code

- `src/emoji_provider/cnn.py` prépare les datasets d’images.
- `scripts/train_transfer.py` construit MobileNetV3, gère le gel, l’entraînement et la sauvegarde.
- `scripts/predict_ensemble.py` recharge MobileNetV3 et utilise ses probabilités.

## À savoir expliquer

1. Quelles connaissances peut-on transférer d’ImageNet vers des emojis ?
2. Pourquoi le learning rate du fine-tuning doit-il être faible ?
3. Pourquoi un modèle moins bon seul peut-il aider un ensemble ?

## Ressources fiables

- [TensorFlow — guide officiel du transfer learning](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [Keras — documentation officielle MobileNet](https://keras.io/2/api/applications/mobilenet/)
- [TensorFlow — classification d’images et augmentation](https://www.tensorflow.org/tutorials/images/classification)
