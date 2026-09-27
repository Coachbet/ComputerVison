from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def append_result(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), **result}
    current = pd.read_csv(path) if path.exists() and path.stat().st_size else pd.DataFrame()
    pd.concat([current, pd.DataFrame([row])], ignore_index=True).to_csv(path, index=False)
