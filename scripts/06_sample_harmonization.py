"""
This step performs sample-level harmonization across all datasets.

What this script does:
- Loads expression, CNA, mutation, and clinical datasets
- Cleans and standardizes Sample_ID values
- Validates required fields using the validator module
- Identifies shared samples across all datasets
- Filters each dataset to keep only common samples
- Saves matched datasets ready for downstream multi-omics analysis
"""

import pandas as pd
from pathlib import Path
from validator import validate_dataset

# =========================
# DEFINE BASE PATH
# =========================
# Set working directory to Desktop
base = Path.home() / "Desktop"


# =========================
# CLEAN SAMPLE_ID (ROBUST VERSION)
# =========================
def clean_sample_id(df, name):
    # Remove hidden spaces from column names
    df.columns = df.columns.str.strip()

    # Ensure Sample_ID column exists
    if "Sample_ID" not in df.columns:
        raise ValueError(f"{name} is missing 'Sample_ID' column")

    # Convert Sample_ID to string and remove leading/trailing spaces
    df["Sample_ID"] = df["Sample_ID"].astype(str).str.strip()

    before = len(df)

    # Remove invalid Sample_ID values:
    # - actual NaN
    # - empty strings
    # - string "nan"
    # - string "none"
    df = df[
        (df["Sample_ID"].notna()) &
        (df["Sample_ID"] != "") &
        (df["Sample_ID"].str.lower() != "nan") &
        (df["Sample_ID"].str.lower() != "none")
    ]

    after = len(df)

    # Report how many rows were removed
    print(f"{name}: removed {before - after} invalid Sample_ID rows")

    return df


# =========================
# MAIN FUNCTION
# =========================
def run():
    print("Loading raw files...")

    # -------- Expression --------
    # Load expression data (long format)
    expr = pd.read_csv(base / "long_expression.csv")

    # Clean Sample_ID values
    expr = clean_sample_id(expr, "Expression")

    # Validate dataset structure
    expr = validate_dataset(expr, "Expression")

    # -------- CNA --------
    # Load CNA data (long format)
    cna = pd.read_csv(base / "cna_long.csv")

    # Clean Sample_ID values
    cna = clean_sample_id(cna, "CNA")

    # Validate dataset structure
    cna = validate_dataset(cna, "CNA")

    # -------- Mutation --------
    # Load mutation data
    mut = pd.read_excel(base / "Mutation.xlsx")

    # Clean Sample_ID values
    mut = clean_sample_id(mut, "Mutation")

    # Validate dataset structure
    mut = validate_dataset(mut, "Mutation")

    # -------- Clinical --------
    # Load clinical data
    clin = pd.read_excel(base / "Clinical&Sample.xlsx")

    # Clean Sample_ID values
    clin = clean_sample_id(clin, "Clinical")

    # Validate dataset (no gene column required here)
    clin = validate_dataset(clin, "Clinical", check_gene=False)

    # =========================
    # FIND COMMON SAMPLES
    # =========================
    print("Finding common samples...")

    # Extract unique sample IDs from each dataset
    expr_samples = set(expr["Sample_ID"].unique())
    cna_samples = set(cna["Sample_ID"].unique())
    mut_samples = set(mut["Sample_ID"].unique())
    clin_samples = set(clin["Sample_ID"].unique())

    # Compute intersection across all datasets
    common_samples = expr_samples & cna_samples & mut_samples & clin_samples

    print(f"Common samples: {len(common_samples)}")

    # =========================
    # FILTER DATASETS
    # =========================
    # Keep only rows with shared Sample_IDs
    expr = expr[expr["Sample_ID"].isin(common_samples)]
    cna = cna[cna["Sample_ID"].isin(common_samples)]
    mut = mut[mut["Sample_ID"].isin(common_samples)]
    clin = clin[clin["Sample_ID"].isin(common_samples)]

    # =========================
    # SAVE OUTPUT FILES
    # =========================
    # Save filtered datasets for next pipeline step
    expr.to_csv(base / "expr_step1.csv", index=False)
    cna.to_csv(base / "cna_step1.csv", index=False)
    mut.to_excel(base / "mut_step1.xlsx", index=False)
    clin.to_excel(base / "clin_step1.xlsx", index=False)

    print("Step 1 complete. Sample-level harmonization finished.")


# =========================
# RUN SCRIPT
# =========================
if __name__ == "__main__":
    run()
