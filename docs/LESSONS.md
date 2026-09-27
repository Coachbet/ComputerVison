### 1. Une image est un tenseur

Une image couleur est représentée par trois matrices d’intensités (rouge, vert,
bleu), parfois accompagnées d’un canal alpha de transparence. Ici, toutes les
images sont composées sur fond blanc, converties en RGB puis redimensionnées de
façon identique. Sans cette étape, le modèle pourrait confondre format de fichier
et fournisseur.

### 2. Traitement classique et features manuelles

Le premier cours présente les convolutions, Sobel et les variations d’intensité.
Notre méthode **HOG** suit cette logique : elle calcule les gradients locaux,
regroupe leur orientation dans des histogrammes, puis décrit les contours de
l’emoji. Ces features sont associées aux histogrammes RGB/HSV avant une
régression logistique.

### 3. Convolution apprise par le CNN

Dans HOG, l’humain choisit la transformation. Dans un **CNN**, les valeurs des
filtres de convolution sont apprises par rétropropagation. Les premières couches
repèrent généralement bords et textures ; les couches suivantes combinent ces
réponses pour reconnaître des formes et styles propres aux fournisseurs.

### 4. Pooling, ReLU et softmax

- **ReLU** introduit une non-linéarité et facilite l’apprentissage des réseaux
  profonds en limitant le problème de gradients trop faibles.
- **Max pooling** réduit la taille des cartes de caractéristiques, diminue les
  calculs et rend la représentation plus robuste aux petits déplacements.
- **Softmax**, uniquement dans la dernière couche, transforme les scores des
  sept fournisseurs en probabilités dont la somme vaut 1.

### 5. LeNet adapté aux emojis

LeNet alterne convolutions et pooling, puis termine par des couches de
classification. Notre version moderne utilise trois convolutions, un pooling
global, une couche dense et une sortie softmax. Elle reste volontairement plus
simple qu’AlexNet afin d’être comprise, entraînable localement et justifiable.

### 6. Limiter l’overfitting

Comme expliqué avec AlexNet dans le troisième cours, le CNN utilise :

- de la **data augmentation** (petites rotations, translations, contraste) ;
- du **dropout**, qui désactive aléatoirement certains neurones à l’entraînement ;
- de l’**early stopping**, qui restaure les poids obtenant la meilleure perte de
  validation ;
- des poids de classes pour compenser la rareté de Mozilla et Messenger.

### 7. Évaluation

L’accuracy mesure la proportion totale de bonnes réponses. La macro-F1 calcule
une F1 par fournisseur puis leur accorde le même poids ; elle est donc plus
informative ici puisque les sept classes sont déséquilibrées. Le score Kaggle
reste séparé du score local et doit être ajouté après la soumission.
