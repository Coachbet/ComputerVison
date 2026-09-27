# Emoji Provider Classification

Projet de Computer Vision — classification du fournisseur d’un emoji (Apple,
Samsung, etc.) à partir de son image.

## Objectif et règles de l’assignment

- Travail en groupe de **3 à 4 étudiants** ; un rapport PDF et une base de code par groupe.
- Tous les membres rejoignent la [compétition Kaggle](https://www.kaggle.com/t/521819a4ff2d4c7a81511fdcb4709a50)
  avec leur compte `@essec.edu`, forment une équipe et soumettent au moins une
  fois le notebook initial exécuté sur Colab.
- Le responsable envoie la composition du groupe à
  [titouan.rigaud@essec.edu](mailto:titouan.rigaud@essec.edu), avec les membres
  en copie, puis dépose rapport et code sur Moodle.
- Seule la meilleure tentative Kaggle compte. Une solution simple, comprise et
  justifiable est préférable à une solution complexe mal maîtrisée.
- Le rapport doit être rédigé par le groupe et exporté en PDF.
- Toute utilisation d’IA doit être déclarée. Compléter
  [`docs/AI_USAGE.md`](docs/AI_USAGE.md) au fil du projet.

## Structure

```text
site/                          # application Streamlit multipage
├── app.py                     # accueil
├── content/courses/         # sept cours reliés au code du projet
├── shared.py                  # fonctions communes
└── pages/                     # cours, expériences, prédiction et IA
configs/baseline.yaml          # paramètres reproductibles
data/{train,test}/             # données locales, ignorées par Git
data/train_labels.csv
docs/                          # méthodologie et journal IA
experiments/results.csv        # registre des essais et scores
notebooks/                     # notebooks du groupe
outputs/                       # modèles et soumissions, ignorés
scripts/{train,predict}.py     # pipeline exécutable
src/emoji_provider/            # code réutilisable
tests/                         # tests rapides
Example_notebook.ipynb         # exemple fourni par l’enseignant
```

## Installation avec uv

Le projet est initialisé avec [`uv`](https://docs.astral.sh/uv/) et accepte
Python 3.11 ou 3.12. Après avoir cloné le dépôt, une seule commande installe la
bonne version de Python si nécessaire, crée `.venv` et restaure exactement les
dépendances de `uv.lock` :

```bash
uv sync
```

Il n’est pas nécessaire d’activer manuellement le virtualenv : préfixer les
commandes par `uv run`. Les commandes classiques du projet sont :

```bash
uv sync                         # crée/met à jour .venv depuis uv.lock
uv add nom-du-paquet             # ajoute une dépendance et actualise le lockfile
uv add --dev nom-du-paquet       # ajoute une dépendance de développement
uv lock                         # recalcule uniquement uv.lock
uv run python --version         # exécute dans l’environnement du projet
```

`uv init` a déjà été exécuté : **il ne faut pas le relancer après le clone**.
Le fichier `requirements.txt` est conservé comme solution de secours pour les
notebooks Colab ; `pyproject.toml` et `uv.lock` restent les références locales.

## Données

Télécharger le ZIP depuis l’onglet **Data** de Kaggle et le décompresser pour
obtenir :

```text
data/train/
data/test/
data/train_labels.csv          # colonnes attendues : Id, Label
```

Les données et archives ne doivent jamais être poussées sur GitHub. Le chargeur
convertit les images en RGB et les redimensionne : tailles différentes, gris et
RGBA sont donc acceptés. Les labels sont joints aux images par `Id`, pas par
l’ordre accidentel des lignes.

Sur Colab : cloner ce dépôt, installer `requirements.txt`, placer les données
avec la même structure et adapter `--data-dir` si nécessaire.

## Baseline reproductible

Six approches sont disponibles : histogrammes RGB/HSV + régression logistique,
HOG + couleurs, CNN LeNet, transfer learning MobileNetV3, boosting de style et
ensemble des meilleurs modèles.

```bash
uv run python scripts/train.py --data-dir data
uv run python scripts/predict.py --data-dir data

# HOG : entraînement puis soumission dédiée
uv run python scripts/train_hog.py --data-dir data
uv run python scripts/predict.py --data-dir data \
  --model outputs/models/hog_logreg.joblib \
  --output outputs/submissions/hog_submission.csv

# CNN LeNet : entraînement puis soumission dédiée
uv run python scripts/train_cnn.py --data-dir data
uv run python scripts/predict_cnn.py --data-dir data

# Modèle de style et métadonnées (meilleur modèle simple)
uv run python scripts/train_style.py --data-dir data

# Transfer learning MobileNetV3
uv run python scripts/train_transfer.py --data-dir data

# Meilleure soumission : boosting + MobileNetV3
uv run python scripts/predict_ensemble.py --data-dir data
```

L’entraînement réalise une séparation stratifiée, affiche accuracy et macro F1,
sauvegarde `outputs/models/baseline.joblib` et ajoute une ligne à
`experiments/results.csv`. La prédiction crée
`outputs/submissions/submission.csv` avec les colonnes exactes `Id,Label`.

```bash
uv run python scripts/train.py --help
uv run python scripts/predict.py --help
head outputs/submissions/submission.csv
```

## Site Streamlit

Le site explique l’objectif, les techniques, les scores et les usages de l’IA.
Sa page **Cours** propose sept chapitres progressifs avec analogies, histoire,
ressources externes, questions de compréhension et liens vers le code exact :

```bash
uv run streamlit run site/app.py
```

Après chaque essai, compléter sa description et son score Kaggle dans
`experiments/results.csv`, puis les décisions dans `docs/METHODOLOGY.md`.

## Démarche conseillée

1. Exécuter et soumettre le notebook fourni une fois par membre sur Colab.
2. Analyser classes, dimensions, canaux, transparence et doublons.
3. Établir le baseline et conserver son score de validation.
4. Tester une amélioration à la fois.
5. Conserver paramètres, scores local/Kaggle et interprétation de chaque essai.
6. Rejouer le projet sur une machine neuve avant la remise.

Attention aux fuites : des variantes proches d’un même emoji peuvent exister
chez plusieurs fournisseurs. Si une famille d’emojis est identifiable,
envisager une validation groupée et expliquer le choix.

## Vérifications

```bash
uv run pytest -q
uv run python -m compileall src scripts site
```

## Checklist de remise

- code exécutable et README à jour ;
- `submission.csv` valide ;
- rapport PDF écrit par le groupe ;
- scores et expériences documentés ;
- usages et prompts d’IA déclarés ;
- noms et rôles complétés ci-dessous.

| Rôle | Nom | E-mail |
|---|---|---|
| Responsable (à confirmer) | À confirmer | À compléter |
| Membre | Lara Normand | À compléter |
| Membre | Kenza Gueddas | À compléter |
| Membre | Oscar Moulet | À compléter |
| Membre | Louis Bettelli | À compléter |
