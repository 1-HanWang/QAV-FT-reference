from pathlib import Path
import hashlib, os, sys

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "core"
os.chdir(ROOT)
sys.path.insert(0, str(CORE))

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

WEIGHTS = ROOT / "weights" / "cora_reference.weights.h5"

import qav_cora_core as core

if __name__ == "__main__":
    print("CORA runnable reference mode")
    print("Configuration: Dense1..Dense7 -> Flatten -> Dense8")
    print("Image pairing order: lexicographic filename order")
    print("Weight file:", WEIGHTS)
    print("Weight SHA256:", sha256(WEIGHTS))
    print("Plot output:", ROOT / "CORA_plots")
    core.evaluate_or_train(
        run_mode="load",
        weights_path=str(WEIGHTS),
        save_after_train=False
    )
