# Qui a dessiné cet emoji ?

Reconnaître le fournisseur d'un emoji (Apple, Facebook, Google, Messenger, Mozilla,
Samsung, WhatsApp) à partir de son image.

**Modèle** : `HistGradientBoostingClassifier` (gradient boosting d'arbres) sur 222 mesures
calculées par image.
**Score en validation** : accuracy **0,960**, macro-F1 **0,965** (1 976 images jamais vues).

## Le cours

Le dossier `site/` est un cours illustré, entièrement consacré à ce modèle : schémas,
analogies, démos interactives, vidéos, histoire du boosting et explication du code.

```bash
python3 -m http.server -d site 8000      # puis ouvrir http://localhost:8000
```

(Les vidéos YouTube demandent un serveur local : ne pas double-cliquer sur `index.html`.)

## Le code

```text
configs/style_boosting.yaml    # les réglages du modèle
src/emoji_provider/
  data.py                      # associe chaque image à son label (par Id)
  features.py                  # image -> 222 mesures (métadonnées, couleurs, histogrammes)
  model.py                     # le HistGradientBoostingClassifier
scripts/run.py                 # entraîne, mesure, prédit le test, écrit le CSV daté
tests/test_features.py         # vérifie les 222 colonnes
site/                          # le cours
```

## Utilisation

Données attendues : `data/train/`, `data/test/`, `data/train_labels.csv` (colonnes `Id`, `Label`).

```bash
uv sync                                        # installe les dépendances
uv run python scripts/run.py --data-dir data   # un lancement = un CSV daté
uv run pytest -q                               # tests
```

`run.py` sépare 80 % / 20 % (stratifié, `random_state=42`), mesure sur les 20 % (accuracy et
macro-F1 affichées), réentraîne sur 100 % des images, prédit le test et écrit **un seul fichier** :

```text
outputs/submission_2026-10-04_22-46_acc0.960.csv     # date, heure, score de validation
```

Rien d'autre n'est sauvegardé : chaque lancement ajoute simplement un CSV (colonnes `Id`, `Label`).

Sans `uv` : `pip install -r requirements.txt`, puis `python scripts/run.py`.
