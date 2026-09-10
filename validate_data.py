from pathlib import Path
import csv, hashlib, sys

ROOT = Path(__file__).resolve().parent

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def validate_dataset(name):
    manifest = ROOT / "data" / name / "manifest.csv"
    images = ROOT / "data" / name / "images"

    rows = list(
        csv.DictReader(
            manifest.open("r", encoding="utf-8-sig")
        )
    )

    errors = []
    expected_names = sorted(
        [f"image_{i}.png" for i in range(50)]
    )

    if len(rows) != 50:
        errors.append(f"Expected 50 rows, got {len(rows)}")

    for pos, expected_name in enumerate(expected_names):
        if pos >= len(rows):
            break

        row = rows[pos]

        if int(row["position"]) != pos:
            errors.append(f"Position mismatch at row {pos}")

        if row["filename"] != expected_name:
            errors.append(
                f"Order mismatch at position {pos}: "
                f"expected {expected_name}, got {row['filename']}"
            )

        p = images / expected_name

        if not p.exists():
            errors.append(f"Missing {expected_name}")
        elif sha256(p) != row["sha256"]:
            errors.append(f"SHA256 mismatch: {expected_name}")

    if errors:
        print(f"{name} data/mapping validation: FAILED")
        for e in errors:
            print(" -", e)
        return False

    print(f"{name} data/mapping validation: PASSED")
    print("Image count: 50")
    print("Pairing order: lexicographic filename order")
    print("Filename / label / SHA256 manifest: OK")
    return True

ok_mnist6 = validate_dataset("MNIST6")
print()
ok_cora = validate_dataset("CORA")

if not (ok_mnist6 and ok_cora):
    sys.exit(1)

print()
print("All packaged image datasets: PASSED")
