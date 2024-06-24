from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parents[0]
TRAINING_DATASET = ROOT_PATH / "data" / "diamonds.csv"
SAVE_PATH_MODELS = ROOT_PATH / "models" / "saved_model"
DB_PATH = ROOT_PATH / "instance" / "flaskr.sqlite"

DEFAULT_ALGORITHM = "xgboost"