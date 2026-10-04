"""Étape 2 du modèle : le gradient boosting d'arbres (HistGradientBoosting)."""
from sklearn.ensemble import HistGradientBoostingClassifier


def build_model(config: dict, seed: int = 42) -> HistGradientBoostingClassifier:
    params = config["model"]
    return HistGradientBoostingClassifier(
        learning_rate=params.get("learning_rate", 0.08),
        max_iter=params.get("max_iter", 350),
        max_leaf_nodes=params.get("max_leaf_nodes", 31),
        l2_regularization=params.get("l2_regularization", 0.1),
        class_weight="balanced",
        random_state=seed,
    )
