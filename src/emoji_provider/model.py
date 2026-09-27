from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_baseline(c: float = 1.0, max_iter: int = 2000) -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(C=c, max_iter=max_iter, class_weight="balanced")),
    ])


def build_model(config: dict, seed: int = 42):
    model_config = config["model"]
    model_type = model_config["type"]
    if model_type == "logistic_regression":
        return build_baseline(model_config["C"], model_config["max_iter"])
    if model_type == "extra_trees":
        return ExtraTreesClassifier(
            n_estimators=model_config.get("n_estimators", 600),
            min_samples_leaf=model_config.get("min_samples_leaf", 1),
            max_features=model_config.get("max_features", "sqrt"),
            class_weight="balanced",
            random_state=seed,
            n_jobs=-1,
        )
    if model_type == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(
            learning_rate=model_config.get("learning_rate", 0.08),
            max_iter=model_config.get("max_iter", 300),
            max_leaf_nodes=model_config.get("max_leaf_nodes", 31),
            l2_regularization=model_config.get("l2_regularization", 0.1),
            class_weight="balanced",
            random_state=seed,
        )
    raise ValueError(f"Unknown model type: {model_type}")
