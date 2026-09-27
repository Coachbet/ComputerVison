Ce journal factuel doit être complété à chaque usage d’un outil d’IA. Le groupe
reste responsable de comprendre, tester et expliquer tout code retenu.

## Entrée 001 — Initialisation du dépôt

- **Date :** 2026-09-27
- **Outil :** OpenAI Codex
- **Demande résumée :** structurer le dépôt GitHub à partir des consignes de
  l’assignment ; créer README, environnement reproductible, `.gitignore`,
  baseline et site Streamlit pour présenter techniques, scores et usages IA.
- **Résultat utilisé :** structure, documentation initiale, pipeline baseline,
  suivi des expériences et application Streamlit.
- **Vérification humaine requise :** relire le code, exécuter les tests et
  l’entraînement sur les vraies données, puis adapter la méthodologie.

## Entrée 002 — Méthodes issues des cours et application Streamlit

- **Date :** 2026-09-27
- **Outil :** OpenAI Codex
- **Demande résumée :** analyser les trois supports dans `lessson/`, entraîner
  plusieurs méthodes dont un CNN, produire leurs prédictions et expliquer les
  notions dans Streamlit.
- **Résultat utilisé :** extraction HOG, CNN type LeNet avec augmentation,
  dropout, pondération des classes et early stopping ; scripts de prédiction,
  soumissions séparées et onglet pédagogique dans Streamlit.
- **Vérification :** entraînement sur une séparation stratifiée, calcul de
  l’accuracy et de la macro-F1, validation du format des CSV et tests locaux.
- **Décision à valider par le groupe :** conserver ces méthodes dans le rapport,
  expliquer honnêtement que le CNN simple est inférieur à la baseline et décider
  si le transfer learning mérite une expérience supplémentaire.

## Entrée 003 — Optimisation compétitive et refonte du site

- **Date :** 2026-09-27
- **Outil :** OpenAI Codex
- **Demande résumée :** dépasser les exemples de cours, produire la meilleure
  solution possible et isoler l’application dans un vrai dossier de site.
- **Résultat utilisé :** audit des formats par fournisseur, features natives et
  de style, Extra Trees, boosting, MobileNetV3 pré-entraîné, ensemble pondéré,
  soumissions dédiées et application Streamlit multipage dans `site/`.
- **Vérification :** comparaison sur la même séparation stratifiée, métriques
  accuracy/macro-F1, test de plusieurs poids d’ensemble et contrôle des CSV.
- **Point de transparence :** les dimensions, modes PNG, tailles de fichiers et
  statistiques alpha sont utilisés comme signatures du processus de rendu. Ce
  choix doit être explicitement décrit et justifié dans le rapport.

## Entrée 004 — Parcours pédagogique du site

- **Date :** 2026-09-27
- **Outil :** OpenAI Codex
- **Demande résumée :** remplacer la simple synthèse des cours par de vrais
  chapitres permettant de comprendre chaque technologie utilisée, avec histoire,
  analogies, vidéos, sites de référence et liens vers le code du projet.
- **Résultat utilisé :** parcours Streamlit en sept chapitres couvrant les pixels,
  features, régression logistique, boosting, CNN, transfer learning et ensemble.
- **Vérification humaine requise :** suivre les ressources, savoir répondre aux
  questions de fin de chapitre et rédiger le rapport avec les mots du groupe.

## Modèle d’entrée à copier

### Entrée XXX — Titre

- **Date :** AAAA-MM-JJ
- **Outil/modèle :**
- **Prompt ou demande résumée :**
- **Fichiers ou idées produits :**
- **Éléments conservés/modifiés/rejetés :**
- **Méthode de vérification par le groupe :**
