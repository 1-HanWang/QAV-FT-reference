# QAV-FT Runnable Reference Implementation

This repository provides runnable methodological reference implementations for representative **ACAS Xu**, **NLP / IMDB**, **MNIST6**, and **CORA** experiments.

The package is intended to demonstrate and reproduce the experimental workflow of the work using fixed reference checkpoints and executable validation scripts. It is a reproducibility-oriented reference release and does **not** constitute a release of the complete internal research codebase.

> **Important:** The numerical results reported below are the validation results of the runnable reference package. They should not be interpreted as a claim that the included checkpoints or the included representative subsets are the exact historical network weights or complete instance collections underlying every result reported elsewhere.

---

## 1. Package contents

A typical public release contains:

```text
.
├── README.md
├── requirements.txt
├── requirements-lock.txt
├── PACKAGE_SHA256.txt
├── REFERENCE_WEIGHTS_SHA256.txt
│
├── run_acas.py
├── run_acas.bat
├── run_nlp.py
├── run_nlp.bat
├── run_mnist6.py
├── run_mnist6.bat
├── run_cora.py
├── run_cora.bat
│
├── validate_data.py
├── validate_runtime.py
│
├── core/
│   ├── qav_acas_core.cp312-win_amd64.pyd
│   ├── qav_nlp_core.cp312-win_amd64.pyd
│   ├── qav_mnist6_core.cp312-win_amd64.pyd
│   └── qav_cora_core.cp312-win_amd64.pyd
│
├── weights/
│   ├── acas_reference.weights.h5
│   ├── nlp_reference.weights.h5
│   ├── mnist6_reference.weights.h5
│   └── cora_reference.weights.h5
│
└── data/
    ├── MNIST6/
    │   ├── images/
    │   └── manifest.csv
    └── CORA/
        ├── images/
        └── manifest.csv
```

The compiled `.pyd` files contain the executable experiment cores. The thin `run_*.py` files provide the public entry points.

---

## 2. Environment

The reference package was validated on a Windows x64 / Python 3.12 environment.

Recommended setup:

```text
Python 3.11
TensorFlow 2.17
NumPy
SymPy
Matplotlib
```

Install the required packages with:

```bash
python -m pip install -r requirements.txt
```

If `requirements-lock.txt` is included, it records the package versions used for the validated release.

---

## 3. Validate the package first

Before running the experiments, check the data and runtime environment:

```bash
python validate_data.py
python validate_runtime.py
```

The validation scripts check the packaged data, expected files, runtime dependencies, and compiled extension modules.

`PACKAGE_SHA256.txt` can be used to check the integrity of the distributed package files.

---

## 4. Run the reference experiments

Run each experiment independently:

```bash
python run_acas.py
python run_nlp.py
python run_mnist6.py
python run_cora.py
```

On Windows, the corresponding `.bat` launchers can also be used.

The default public workflow loads the provided fixed reference checkpoint and performs evaluation without updating the model weights.

---

## 5. Reference-result summary

The four runnable reference experiments use a common reporting structure:

- number of evaluation samples;
- number of correctly classified samples;
- clean classification accuracy;
- correctly classified samples satisfying the relevant bound-separation check;
- agreement between correct classification and the sampled/reference bound-separation result.

| Experiment | Evaluation samples | Correctly classified | Clean accuracy | Bound separation among correct samples | Agreement |
|---|---:|---:|---:|---:|---:|
| **ACAS Xu** | 100 | 100 / 100 | **100.00%** | 100 / 100 | **100.00%** |
| **NLP / IMDB** | 100 | 65 / 100 | **65.00%** | 59 / 65 | **90.77%** |
| **MNIST6** | 50 | 45 / 50 | **90.00%** | 45 / 45 | **100.00%** |
| **CORA** | 50 | 49 / 50 | **98.00%** | 49 / 49 | **100.00%** |

The exact numerical meaning of the bound-separation column is described separately for each experiment below.

---

## 6. ACAS Xu reference experiment

The ACAS Xu runner evaluates the fixed reference configuration on 100 samples.

### Reference evaluation results

| Metric | Result |
|---|---:|
| Evaluation samples | 100 |
| Correctly classified samples | 100 / 100 |
| Clean classification accuracy | 100.00% |
| Samples satisfying the bound-separation condition | 100 / 100 |
| Overall bound-separation pass rate | 100.00% |
| Correctly classified samples satisfying the bound-separation condition | 100 / 100 |
| Bound-separation agreement among correctly classified samples | 100.00% |


---

## 7. NLP / IMDB-based reference experiment

The NLP runner is an **IMDB-based binary-classification reference implementation**. It should not be interpreted as an official SafeNLP implementation.

The active reference configuration uses a 30-dimensional input representation, a hidden layer with 128 units, and a 2-class output.

### Reference evaluation results

| Metric | Result |
|---|---:|
| Evaluation samples | 100 |
| Correctly classified samples | 65 / 100 |
| Clean classification accuracy | 65.00% |
| Correctly classified samples satisfying bound-separation condition | 59 / 65 |
| Sampled bound-separation agreement | 90.77% |

The fixed reference checkpoint therefore reproduces a classification accuracy of **65.00%**. Among the 65 correctly classified samples, 59 satisfy bound-separation condition.

---

## 8. MNIST6 reference experiment

The MNIST6 runner uses the fixed reference checkpoint together with the packaged 50-image evaluation set.

### Reference evaluation results

| Metric | Result |
|---|---:|
| Evaluation samples | 50 |
| Correctly classified samples | 45 / 50 |
| Clean classification accuracy | 90.00% |
| Correctly classified samples satisfying bound-separation condition | 45 / 45 |
| Sampled bound-separation agreement | 100.00% |
| Correctly classified samples failing sampled separation | 0 |


### Bound-separation criterion

For a correctly classified sample with target class \(y\), the comparison is:

\[
L_y(x) > \max_{j \ne y} U_j(x)
\]

where:

- \(L_y(x)\) is the lower-bound expression associated with the target class;
- \(U_j(x)\) denotes the upper-bound expression of a non-target class;
- the target class's own upper bound is excluded from the comparison.

The interval propagation used by this reference workflow stops at the input of the final classification layer. The resulting range is then evaluated.

Therefore, **45/45 = 100%** means 100% sampled bound-separation agreement among the correctly classified samples. It is not described as formal continuous-domain verification accuracy.

### MNIST6 data ordering

The packaged image/label mapping follows the fixed **lexicographic filename order** used by the validated reference package, for example:

```text
image_0.png
image_1.png
image_10.png
...
```

The mapping is fixed in the packaged manifest so that filesystem enumeration order cannot change the evaluation pairing.

---

## 9. CORA reference experiment

The CORA runner uses the fixed reference checkpoint and the packaged 50-image reference evaluation set.
The 50-image set included in this repository is a runnable reference evaluation set for executable validation of the implementation and should
not be confused with the 200 CORA instances reported in the paper.


### Current reference architecture

The runnable reference configuration follows the current MNIST6-style evaluation framework:

```text
Input image
    ↓
Dense1 + ReLU
    ↓
Dense2 + ReLU
    ↓
Dense3 + ReLU
    ↓
Dense4 + ReLU
    ↓
Dense5 + ReLU
    ↓
Dense6 + ReLU
    ↓
Dense7 + ReLU
    ↓
Flatten
    ↓
Dense8 (10-class output)
```

### Reference evaluation results

| Metric | Result |
|---|---:|
| Evaluation samples | 50 |
| Correctly classified samples | 49 / 50 |
| Clean classification accuracy | 98.00% |
| Correctly classified samples satisfying bound-separation condition | 49 / 49 |
| Sampled bound-separation agreement | 100.00% |
| Correctly classified samples failing sampled separation | 0 |

All 49 correctly classified samples satisfy the bound-separation condition.

### Bound-separation criterion

The CORA reference workflow uses the same target-vs-non-target comparison:

\[
L_y(x) > \max_{j \ne y} U_j(x)
\]

The target class upper bound is excluded from both the comparison and the plotted set of non-target upper bounds.

For each correctly classified sample, interval propagation is performed up to the input of `Dense8`. The resulting interval is used bound-separation evaluation.

Accordingly, **49/49 = 100%** is reported as sampled bound-separation agreement, not as formal continuous-domain verification accuracy.

### CORA data ordering

As with MNIST6, the packaged CORA image/label mapping is fixed using the validated lexicographic filename ordering and the corresponding manifest.

### CORA plots

Running the CORA reference experiment generates plots in:

```text
CORA_plots/
```

The plots compare:

- the target-class lower-bound curve;
- the upper-bound curves of the non-target classes;
- the maximum and minimum non-target upper bounds.

The target class upper bound is intentionally omitted.

---

## 10. Reference checkpoints

The `weights/` directory contains fixed reference checkpoints used for deterministic executable validation.

They are provided so that a user can:

1. validate the package installation;
2. reproduce the reference-run statistics;
3. evaluate the implemented workflow without depending on a new random training run.

Unless explicitly documented otherwise, these files should be referred to as:

> **reference checkpoints from validated runs**

---

## 11. Compiled experiment cores

The experiment cores are distributed as compiled Cython / Windows extension modules (`.pyd`).

The public runners import these compiled modules and execute the reference workflows without requiring the corresponding internal Python research source files.

This packaging choice is intended to provide runnable reproducibility material while keeping the scope of the public release distinct from the complete internal research codebase.

The `.pyd` files should be treated as compiled executable extensions, not as a cryptographic source-protection mechanism.

---

## 12. Reproducibility scope

This repository is a **runnable methodological reference implementation**.

It provides executable examples for:

- loading or generating the relevant reference inputs;
- loading fixed validated checkpoints;
- evaluating the neural-network classifiers;
- constructing the approximation/bound expressions used by the reference workflows;
- comparing target-class lower bounds with non-target upper bounds;
- reporting automatic classification and bound-separation statistics;
- generating the corresponding plots where enabled.

The package is designed to support inspection and independent execution of the experimental methodology. It is not intended to be a release of the full internal research codebase or of unrelated unpublished research components.

---

## 13. Generated output directories

Some runners generate plots or other runtime output directories. These outputs are created during execution and generally do not need to be committed to the repository.

Examples include:

```text
CORA_plots/
MNIST6_last_layer_input_range_plots/
acas_xu_right_plots/
NLP_right_plots/
```

The exact directory names can depend on the packaged runner version.

---

## 14. Suggested validation workflow

For a fresh copy of the repository:

```bash
python -m pip install -r requirements.txt

python validate_data.py
python validate_runtime.py

python run_acas.py
python run_nlp.py
python run_mnist6.py
python run_cora.py
```

A successful end-to-end validation should complete all four runners and reproduce the reference-package statistics summarized above.

---

## 15. SHA256
`PACKAGE_SHA256.txt` records SHA256 integrity information for the
distributed package files, while `REFERENCE_WEIGHTS_SHA256.txt` records
the SHA256 hashes of the fixed reference checkpoints.

---

## 16. Scope and Boundaries
`Platform:` This reference package is compiled and validated exclusively for Windows x64 / Python 3.12. Cross-platform builds, including Linux builds, are outside the scope of this release and are not provided.

`Format:` This repository provides a runnable methodological reference implementation in its documented native format. ONNX/VNNLIB benchmark packages are not part of this release, and the repository is not intended to serve as a VNN-COMP submission or interoperability package.

`Source Code:` The public release provides compiled binary extensions (.pyd) rather than the complete internal Python source tree. Uncompiled internal source code, build scripts, development files, and unpublished research components are not included in the public repository.

`Extensions:` The authors do not provide modified, extended, customized, or platform-specific versions of the reference package on request.

`Support and availability:` The materials provided here constitute the complete public release of the reference implementation. The paper states that datasets and code are available from the corresponding author upon reasonable request. This does not mean that all requests will be fulfilled, nor does it create an entitlement to additional software, source code, datasets, builds, conversions, or technical support beyond the scope of the published work. Requests are evaluated individually and may be declined.
