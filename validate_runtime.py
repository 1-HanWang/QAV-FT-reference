from pathlib import Path
import hashlib, importlib.util, platform, sys

ROOT = Path(__file__).resolve().parent
print("Python:", sys.version.split()[0])
print("System:", platform.system(), platform.machine())

required = ["tensorflow", "numpy", "sympy", "matplotlib", "h5py"]
missing = []
for m in required:
    ok = importlib.util.find_spec(m) is not None
    print(f"{m}: {'OK' if ok else 'MISSING'}")
    if not ok:
        missing.append(m)

core_names = [
    "qav_acas_core",
    "qav_nlp_core",
    "qav_mnist6_core",
    "qav_cora_core",
]

cores = []
for name in core_names:
    matches = (
        list((ROOT / "core").glob(name + "*.pyd"))
        + list((ROOT / "core").glob(name + "*.so"))
    )
    print(f"{name}: {[p.name for p in matches]}")
    if len(matches) == 1:
        cores.append(matches[0])

errors = []
manifest = ROOT / "REFERENCE_WEIGHTS_SHA256.txt"

for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    digest, rel = line.split(None, 1)
    p = ROOT / rel.strip()
    if not p.exists():
        errors.append(f"Missing weight: {rel.strip()}")
    elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
        errors.append(f"Weight hash mismatch: {rel.strip()}")

expected_weights = [
    ROOT / "weights" / "acas_xu_reference.weights.h5",
    ROOT / "weights" / "nlp_reference.weights.h5",
    ROOT / "weights" / "mnist6_reference.weights.h5",
    ROOT / "weights" / "cora_reference.weights.h5",
]

for p in expected_weights:
    if not p.exists():
        errors.append(f"Missing reference weight: {p.name}")

if missing:
    errors.append("Missing modules: " + ", ".join(missing))

if len(cores) != 4:
    errors.append(f"Expected 4 compiled cores, found {len(cores)}")

if errors:
    print("Runtime/package validation: FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("Reference weights: SHA256 OK")
print("Runtime/package validation: PASSED")
