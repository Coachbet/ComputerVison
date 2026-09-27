## Baseline : histogrammes de couleurs + régression logistique

Chaque image est convertie en RGB, redimensionnée à 96 × 96, puis décrite par
des histogrammes RGB et HSV normalisés. Une régression logistique équilibrée
prédit le fournisseur. Cette approche vérifie rapidement tout le pipeline avant
d’investir dans un réseau de neurones.

### Pourquoi ce choix ?

- Les fournisseurs se distinguent souvent par leur palette et leur rendu.
- La représentation accepte différentes tailles et les canaux RGB/RGBA/gris.
- Le modèle sert de référence simple, reproductible et explicable.

## HOG + couleurs

HOG résume les orientations des gradients dans de petites cellules. Il capture
les contours et détails de dessin que les histogrammes de couleur ignorent. Les
features HOG et couleur alimentent la même régression logistique équilibrée.

## CNN type LeNet

Le CNN apprend ses filtres directement sur les pixels. Trois convolutions avec
ReLU extraient des motifs de complexité croissante ; le pooling réduit la
résolution ; dropout, augmentation et early stopping limitent l’overfitting.
La sortie softmax prédit l’un des sept fournisseurs.

## Résultats locaux actuels

| Méthode | Accuracy | Macro-F1 | Interprétation |
|---|---:|---:|---|
| Histogrammes RGB/HSV + logistique | 0,780 | 0,797 | Meilleure référence actuelle |
| HOG + couleurs + logistique | 0,757 | 0,749 | Les contours n’améliorent pas la couleur |
| CNN type LeNet | 0,426 | 0,426 | Fonctionnel mais sous-entraîné/sans pré-entraînement |
| MobileNetV3 pré-entraîné | 0,658 | 0,640 | Meilleur CNN, signal visuel complémentaire |
| Style + métadonnées + boosting | 0,960 | 0,965 | Dimensions, alpha, format et rendu global |
| Ensemble boosting + MobileNetV3 | **0,963** | **0,967** | Meilleur résultat local actuel |

Ces résultats montrent qu’un modèle plus complexe n’est pas automatiquement
meilleur. Les dimensions natives, le mode PNG, la transparence, la taille du
fichier et les statistiques de couleur constituent une signature du pipeline de
rendu de chaque fournisseur. Leur utilisation est assumée et doit être déclarée
dans le rapport. MobileNetV3 apporte un signal visuel indépendant ; un mélange
50/50 de ses probabilités avec celles du boosting corrige quelques erreurs.

## Choix final actuel

Le boosting seul est la solution explicable et robuste. L’ensemble avec
MobileNetV3 est la meilleure solution locale. Les deux doivent être soumis à
Kaggle : le score public déterminera si l’amélioration se généralise au test.

Pour chaque expérience, noter l’hypothèse, le protocole, les paramètres, les
scores validation/Kaggle, le coût de calcul et l’interprétation du résultat.
