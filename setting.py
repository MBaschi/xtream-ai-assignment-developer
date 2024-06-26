from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parents[0]

SAVE_PATH_MODELS = ROOT_PATH / "models" / "saved_model"
DB_PATH = ROOT_PATH / "instance" / "app_db.sqlite"
DEFAULT_DATASET = ROOT_PATH / "data" / "diamonds.csv"
DEFAULT_ALGORITHM = "XgBoost"
