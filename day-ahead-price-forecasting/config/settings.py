from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = BASE_DIR / "data"


RAW_DATA_DIR = DATA_DIR / "raw"


PROCESSED_DATA_DIR = DATA_DIR / "processed"


MODELS_DIR = BASE_DIR / "models"


REPORTS_DIR = BASE_DIR / "reports"


FIGURES_DIR = REPORTS_DIR / "figures"


BACKTEST_DIR = REPORTS_DIR / "backtesting"


DASHBOARD_DIR = REPORTS_DIR / "dashboard"