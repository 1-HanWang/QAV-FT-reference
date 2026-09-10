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

WEIGHTS = ROOT / "weights" / "acas_xu_reference.weights.h5"
import qav_acas_core as core
if __name__ == "__main__":
    print("ACAS Xu reference mode")
    print("Weight file:", WEIGHTS)
    print("Weight SHA256:", sha256(WEIGHTS))
    core.main(mode="load", weights_path=str(WEIGHTS), save_after_training=False)
