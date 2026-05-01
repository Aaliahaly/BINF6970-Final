"""
This step performs gene-level harmonization across multi-omics datasets.

What this script does:
- Loads Step 1 filtered datasets (sample-level harmonized)
- Standardizes gene symbols (Hugo_Symbol) across all datasets
- Identifies common genes shared across expression, CNA, and mutation data
- Filters each dataset to retain only these shared genes
- Outputs aligned datasets ready for multi-omics integration
"""

import pandas as pd
from pathlib import Path

# =========================
# DEFINE BASE PATH
# =========================
base = Path.home() / "Desktop"


def run():
    print("Loading Step 1 files...")

    # -------- Load datasets --------
    expr = pd.read_csv(base / "expr_step1.csv")   # Expression data
    cna = pd.read_csv(base / "cna_step1.csv")     # CNA data
    mut = pd.read_excel(base / "mut_step1.xlsx")  # Mutation data

    # =========================
    # STANDARDIZE GENE SYMBOLS
    # =========================
    for df in [expr, cna, mut]:
        # Clean column names
        df.columns = df.columns.str.strip()

        # Standardize Hugo_Symbol:
        # - convert to string
        # - remove spaces
        # - enforce uppercase
        df["Hugo_Symbol"] = (
            df["Hugo_Symbol"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # =========================
    # FIND COMMON GENES
    # =========================
    print("Finding common genes...")

    # Extract unique gene sets
    expr_genes = set(expr["Hugo_Symbol"].unique())
    cna_genes = set(cna["Hugo_Symbol"].unique())
    mut_genes = set(mut["Hugo_Symbol"].unique())

    # Compute intersection across all datasets
    common_genes = expr_genes & cna_genes & mut_genes

    print(f"Common genes: {len(common_genes)}")

    # =========================
    # FILTER DATASETS
    # =========================
    # Keep only shared genes
    expr = expr[expr["Hugo_Symbol"].isin(common_genes)]
    cna = cna[cna["Hugo_Symbol"].isin(common_genes)]
    mut = mut[mut["Hugo_Symbol"].isin(common_genes)]

    # =========================
    # SAVE OUTPUT FILES
    # =========================
    expr.to_csv(base / "expr_step2.csv", index=False)
    cna.to_csv(base / "cna_step2.csv", index=False)
    mut.to_excel(base / "mut_step2.xlsx", index=False)

    print("Step 2 complete. Gene-level harmonization finished.")


# =========================
# RUN SCRIPT
# =========================
if __name__ == "__main__":
    run()
