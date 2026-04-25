from src.dataset import build_dataset
from src.models import train_models
from src.utils import ensure_dirs
# Make sure folders exist
ensure_dirs()

# Your merged file
file_path = "data/data_record.csv"   # <-- change name if needed

print(f"Loading data from: {file_path}")

# Build dataset (this already handles windowing + gaps)
X = build_dataset(file_path)

if len(X) == 0:
    raise Exception("No valid windows extracted. Check your data or window parameters.")

print(f"Dataset shape: {X.shape}")

# Train models
svm, iso = train_models(X)

print("✅ Training complete!")