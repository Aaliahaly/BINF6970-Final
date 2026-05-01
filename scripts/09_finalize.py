"""
This step performs final harmonization across all datasets after previous cleaning and mapping steps.

What this script does:
- Loads Step 3 datasets (already standardized and mapped)
- Performs final sample-level alignment across all datasets
- Performs final gene-level alignment across expression, CNA, and mutation data
- Ensures all datasets are fully synchronized
- Outputs final matched datasets ready for integration and analysis
"""

import pandas as pd
from pathlib import Path

# =========================
# DEFINE BASE PATH
# =========================
base = Path.home() / "Desktop"


def run():
    print("Loading Step 3 files...")

    # -------- Load datasets --------
    expr = pd.read_csv(base / "expr_step3.csv")   # Expression data
    cna = pd.read_csv(base / "cna_step3.csv")     # CNA data
    mut = pd.read_excel(base / "mut_step3.xlsx")  # Mutation data
    clin = pd.read_excel(base / "clin_step1.xlsx")  # Clinical data (sample-aligned)

    # =========================
    # CLEAN COLUMN NAMES
    # =========================
    for df in [expr, cna, mut, clin]:
        df.columns = df.columns.str.strip()

    # =========================
    # FINAL SAMPLE ALIGNMENT
    # =========================
    print("Performing final sample alignment...")

    # Extract unique Sample_IDs
    expr_samples = set(expr["Sample_ID"].unique())
    cna_samples = set(cna["Sample_ID"].unique())
    mut_samples = set(mut["Sample_ID"].unique())
    clin_samples = set(clin["Sample_ID"].unique())

    # Compute intersection across all datasets
    common_samples = expr_samples & cna_samples & mut_samples & clin_samples

    # Filter datasets to keep only shared samples
    expr = expr[expr["Sample_ID"].isin(common_samples)]
    cna = cna[cna["Sample_ID"].isin(common_samples)]
    mut = mut[mut["Sample_ID"].isin(common_samples)]
    clin = clin[clin["Sample_ID"].isin(common_samples)]

    # =========================
    # FINAL GENE ALIGNMENT (SAFETY CHECK)
    # =========================
    # Ensure consistency across expression, CNA, and mutation datasets

    expr_genes = set(expr["Hugo_Symbol"].unique())
    cna_genes = set(cna["Hugo_Symbol"].unique())
    mut_genes = set(mut["Hugo_Symbol"].unique())

    # Compute shared genes
    common_genes = expr_genes & cna_genes & mut_genes

    # Filter datasets to keep only shared genes
    expr = expr[expr["Hugo_Symbol"].isin(common_genes)]
    cna = cna[cna["Hugo_Symbol"].isin(common_genes)]
    mut = mut[mut["Hugo_Symbol"].isin(common_genes)]

    # =========================
    # SAVE FINAL OUTPUTS
    # =========================
    expr.to_csv(base / "expr_FINAL.csv", index=False)
    cna.to_csv(base / "cna_FINAL.csv", index=False)
    mut.to_excel(base / "mut_FINAL.xlsx", index=False)
    clin.to_excel(base / "clin_FINAL.xlsx", index=False)

    print("Step 4 complete. Final aligned files saved.")


# =========================
# RUN SCRIPT
# =========================
if __name__ == "__main__":
    run()
