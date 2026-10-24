# GENIE Brain-Met Megaplan

Bring the `genie_brain_met` project to a finished, publication-ready state by: staging the analytic data, integrating the external pull/SHAP scripts, executing all 4 analysis notebooks, enforcing journal figure standards, and wiring the SHAP dashboard to real model output.

---

## Repositories / directories in scope

| Location | Role |
|---|---|
| `/Users/robertjames/loc/repos/portfolio_ai_engineering_projects/genie_brain_met/` | **Primary repo** — all outputs land here |
| `/Users/robertjames/genie_build_shap_dashboard_pull_datasets/` | External scripts to integrate (pull, SHAP, dashboard UI) |

---

## Phase 0 — Environment

**Goal:** one conda env with every import the notebooks need; registered as a Jupyter kernel.

### 0-A. Extend `tcga-analysis` env
```bash
conda activate tcga-analysis
pip install statsmodels==0.14.2 lifelines==0.29.0 lightgbm==4.3.0 \
            optuna==3.6.1 shap==0.45.1 scikit-survival==0.22.2 \
            openpyxl==3.1.2 nbconvert nbformat
```
Reconcile with existing pins before running (check `conda list` first; do **not** upgrade numpy above 1.26.x or scikit-learn above 1.4.x — `scikit-survival` requires those bounds per `requirements.txt`).

### 0-B. Register kernel
```bash
python -m ipykernel install --user --name genie-brainmet --display-name "genie-brainmet"
```

### 0-C. Smoke test
```python
import pandas, numpy, scipy, sklearn, lifelines, statsmodels
import xgboost, lightgbm, optuna, shap, sksurv, openpyxl
```

---

## Phase 1 — Data staging

**Goal:** `data/processed/` populated with all analytic CSVs `_lib.load_cohort()` needs.

### 1-A. Copy GENIE analytic frame
```
src/exploratory data analysis/retrieved_genie_data/
  extracted_variables_genie_data.csv          -> data/processed/
  extracted_variables_genie_top_genes.txt     -> data/processed/
  extracted_variables_genie_gene_prev_brain_met.csv -> data/processed/
  extracted_variables_genie_dictionary.csv    -> data/processed/
```

### 1-B. Copy MSK analytic frame
```
src/exploratory data analysis/msk_retrieved_data/
  extracted_variables_breast_msk_2018_data.csv        -> data/processed/
  extracted_variables_breast_msk_2018_top_genes.txt   -> data/processed/
  extracted_variables_breast_msk_2018_gene_prev_brain_met.csv -> data/processed/
```

### 1-C. Patch `PROJ` in all notebooks
Each notebook hard-codes:
```python
PROJ = "/Users/robertjames/Documents/Documents - Robert's iMac/Research Projects/..."
```
Replace with a dynamic path relative to the repo root:
```python
import pathlib
PROJ = pathlib.Path(__file__).resolve().parents[1]  # repo root
```
Redirect these sub-paths inside the notebooks:
- `PROJ/data/processed/` → `data/processed/` (already correct after 1-A)
- `PROJ/manuscript components/figures/` → `manuscript components/genie/`
- `PROJ/src/modeling/genie/aimN/` → `src/modeling/genie/aimN/`

Create output directories if missing: `reports/figures/aim{1,2,3,ml_benchmark}/`, `manuscript components/genie/aim{1,2,3}/`, `src/modeling/genie/aim{1,2,3}/`.

---

## Phase 2 — Integration of external pull scripts

**Goal:** move data-acquisition scripts from the scratch directory into the repo.

### 2-A. Move R pull scripts
Copy into `src/data collection and processing/`:
- `pull_brca_clinical.R`
- `pull_brca_genetics.R`
- `pull_tcga_brca_mutations.R`
- `pull_tcga_brca.R`

Update `out_dir` in each from `/Users/robertjames` to `../../data/raw/` (relative to script location) or accept a CLI `--out_dir` argument.

### 2-B. Move Python SHAP script
Copy `plot_shap.py` → `src/modeling/plot_shap.py`.

### 2-C. Move R SHAP script
Copy `shap_feature_explainer.R` → `src/modeling/shap_feature_explainer.R`.

### 2-D. Move dashboard UI
Copy `cohort-shap-dashboard/index.html` → `reports/dashboard/index.html`.

---

## Phase 3 — Execute notebooks

Run each in order using the registered kernel. Use `nbconvert` to execute and save the output notebook (with cell outputs) in place.

```bash
BASE=/Users/robertjames/loc/repos/portfolio_ai_engineering_projects/genie_brain_met
NB="jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=genie-brainmet \
    --ExecutePreprocessor.timeout=3600"

cd "$BASE"
$NB notebooks/descriptiveplots.ipynb
$NB notebooks/timebrainmettplots.ipynb
$NB notebooks/osplots.ipynb
$NB notebooks/coxvsaft_error_os.ipynb
$NB src/modeling/survival_and_xgb_analysis.ipynb
# retrieval_metadata_recode.ipynb — SKIP (doc-only, missing raw data)
```

**Per-notebook acceptance criteria:**

| Notebook | Required outputs |
|---|---|
| `descriptiveplots.ipynb` | Table 1 CSV; cohort demographics figure; gene prevalence bar chart |
| `timebrainmettplots.ipynb` | KM curves (Aim 2); log-rank p-values; Cox/AFT summary CSVs |
| `osplots.ipynb` | KM curves (Aim 3); Cox/AFT summary CSVs |
| `coxvsaft_error_os.ipynb` | XGBoost-AFT C-index; model error comparison figure; SHAP values CSV |
| `survival_and_xgb_analysis.ipynb` | Combined KM/Cox/Fine-Gray/XGBoost-AFT outputs |

Fix any errors encountered (missing columns, import failures, path issues) before proceeding to the next notebook. Document fixes in `wiki/Known-Issues-and-Gaps.md`.

---

## Phase 4 — Publication figure standards

Apply to **every PNG** emitted by the notebooks. Standard: Nature Medicine / JCO.

### Rules
| Property | Requirement |
|---|---|
| Resolution | ≥ 300 dpi |
| Background | White (`#ffffff`) |
| Gridlines | None (remove major and minor) |
| Font | Arial or Helvetica, size ≥ 8pt |
| Color palette | Colorblind-safe; preferred: `#1f77b4` (blue), `#ff7f0e` (orange), `#2ca02c` (green), `#d62728` (red) — avoid pure red/green together |
| Legend | Inside or right of plot; no box border |
| Axes | Spines: left + bottom only; ticks outward |
| Format | Save both `.png` (300 dpi) and `.pdf` (vector) |

### Implementation
Create `src/reporting/fig_style.py`:
```python
import matplotlib as mpl, matplotlib.pyplot as plt

PALETTE = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']

def apply_pub_style():
    mpl.rcParams.update({
        'font.family': 'Arial',
        'font.size': 9,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.facecolor': 'white',
        'legend.frameon': False,
    })
    plt.rcParams['axes.prop_cycle'] = mpl.cycler(color=PALETTE)
```

Import `apply_pub_style()` at the top of each notebook (and each `src/modeling/*.py` script) and call it before any plot is created.

Add a post-processing step to re-export any existing PNGs that don't meet the standard using Pillow (set DPI metadata) or re-run plot cells.

---

## Phase 5 — SHAP dashboard

**Goal:** wire `reports/dashboard/index.html` (the "trace" dark-theme UI) to the real XGBoost-AFT SHAP output.

### 5-A. Generate SHAP data
After `coxvsaft_error_os.ipynb` runs and saves `xgb_model.joblib` (or the AFT model JSON):
```bash
python src/modeling/plot_shap.py \
  --model_dir src/modeling/genie/ml_benchmark \
  --infile data/processed/extracted_variables_genie_data.csv \
  --time_col time_brain_met_months \
  --event_col brain_met_event \
  --t 36 \
  --covariates top5_any_mutated receptor_primary_cat grade_ord age_dx_num ...
```
This writes `shap_summary.png` and the SHAP values array.

Also run `shap_feature_explainer.R` to produce `shap_ranked_features.csv` and `shap_dependence_*.png`.

### 5-B. Convert SHAP output to dashboard JSON
Write `src/reporting/shap_to_dashboard_json.py` that:
1. Reads `shap_ranked_features.csv` (feature, mean_abs_shap)
2. Reads the per-sample SHAP contributions matrix
3. Emits `reports/dashboard/data/shap_data.json` in the format the dashboard JS expects

Inspect `index.html` to determine the exact JSON schema (look for `fetch(` calls or inline data objects).

### 5-C. Update dashboard to load from file
Replace any hardcoded placeholder data in `index.html` with a `fetch('data/shap_data.json')` call. Ensure the dashboard works with `python -m http.server` from `reports/dashboard/`.

### 5-D. Verify dashboard
Open `http://localhost:8000` — confirm feature list, attribution bars, and patient-level views render correctly from real data.

---

## Phase 6 — Cleanup and status

### 6-A. Update `STATUS.md`
Mark these items complete:
- `[ ]` Run the ETL / data staging (`data/processed/` now populated)
- `[ ]` Generate missing Aim 2 & 3 survival / XGBoost-AFT result tables
- `[ ]` Publication figures finalized in `reports/figures/`

### 6-B. Update `ARCHITECTURE.md`
- Document the `data/processed/` population step
- Add the SHAP dashboard to the output map
- Note that pull scripts are now in `src/data collection and processing/`

### 6-C. Update `README.md`
Add a **Quick Start** section:
```
conda activate tcga-analysis
# Stage data
cp "src/exploratory data analysis/retrieved_genie_data/"* data/processed/
# Run notebooks
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=genie-brainmet \
  notebooks/descriptiveplots.ipynb ...
# View dashboard
cd reports/dashboard && python -m http.server
```

### 6-D. Update `data/README.md`
Document provenance of each file in `data/processed/`.

---

## Acceptance criteria (overall)

- [ ] `data/processed/` contains all 3-cohort analytic CSVs and top-genes files
- [ ] All 4 main notebooks execute to completion with no unhandled exceptions
- [ ] `reports/figures/aim{1,2,3,ml_benchmark}/` contains PNG + PDF for every figure
- [ ] All figures: 300 dpi, white bg, no gridlines, font ≥8pt, colorblind-safe palette
- [ ] `src/modeling/genie/aim{1,2,3}/` contains result CSVs (Cox summary, logrank pairs, AFT comparison)
- [ ] `manuscript components/genie/aim{1,2,3}/` updated with latest PDFs
- [ ] SHAP dashboard (`reports/dashboard/index.html`) loads and displays real SHAP data
- [ ] External pull scripts and SHAP scripts moved into the repo
- [ ] `STATUS.md` updated; `README.md` has working Quick Start

---

## Risks / dependencies

| Risk | Mitigation |
|---|---|
| `scikit-survival` requires libomp (macOS) | `brew install libomp` if import fails |
| XGBoost AFT needs `libomp` too | Same fix |
| SHAP dashboard JSON schema unknown until runtime | Inspect `index.html` JS before writing converter |
| TCGA data not in `data/processed/` (no `extracted_variables_tcga_data.csv`) | TCGA cohort may not run in modeling scripts; pull fresh via `pull_tcga_brca.R` or scope to GENIE only |
| Notebook `PROJ` patching may miss subdirectory refs | Search notebooks for all string literals containing the iCloud path |
