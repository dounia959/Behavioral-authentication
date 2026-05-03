from src.dataset import build_dataset
from src.models import train_models
from src.utils import ensure_dirs


ensure_dirs()

file_path = "data/data_record.csv"

print(f"Loading data from: {file_path}")

X = build_dataset(file_path)

if len(X) == 0:
    raise Exception("No valid windows extracted. Check your data or window parameters.")

print(f"Dataset shape: {X.shape}")

train_models(X)

print("Training complete.")
