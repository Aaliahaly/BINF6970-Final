"""
This step standardizes gene identifiers across all datasets using HGNC reference mapping.

What this script does:
- Loads Step 2 datasets (already sample- and gene-harmonized)
- Standardizes gene symbols (Hugo_Symbol) to a consistent format
- Builds an HGNC-based mapping dictionary using:
    - official gene symbols
    - alias symbols
    - previous gene names
- Maps all genes to Entrez Gene IDs
- Removes unmapped entries to ensure consistency
- Outputs cleaned datasets with unified gene identifiers
"""

import pandas as pd
from pathlib import Path
from validator import validate_hgnc

# =========================
# DEFINE BASE PATH
# =========================
base = Path.home() / "Desktop"


def run():
    print("Loading Step 2 files...")

    # -------- Load datasets --------
    expr = pd.read_csv(base / "expr_step2.csv")   # Expression data
    cna = pd.read_csv(base / "cna_step2.csv")     # CNA data
    mut = pd.read_excel(base / "mut_step2.xlsx")  # Mutation data

    # =========================
    # STANDARDIZE GENE SYMBOLS
    # =========================
    for df in [expr, cna, mut]:
        # Clean column names
        df.columns = df.columns.str.strip()

        # Normalize gene symbols:
        # - convert to string
        # - remove whitespace
        # - enforce uppercase
        df["Hugo_Symbol"] = (
            df["Hugo_Symbol"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # =========================
    # LOAD HGNC REFERENCE
    # =========================
    print("Loading HGNC mapping file...")

    # Validate HGNC file structure and load it
    hgnc = validate_hgnc()

    # =========================
    # BUILD MAPPING DICTIONARY
    # =========================
    mapping = {}

    # -------- Official symbols --------
    # Direct mapping: official symbol → Entrez ID
    mapping.update(dict(zip(hgnc["symbol"], hgnc["entrez_id"])))

    # -------- Alias symbols --------
    # Map alternative gene names to Entrez IDs
    if "alias_symbol" in hgnc.columns:
        alias_df = hgnc[["alias_symbol", "entrez_id"]].dropna()

        for _, row in alias_df.iterrows():
            # Some rows contain multiple aliases separated by "|"
            for alias in str(row["alias_symbol"]).split("|"):
                alias = alias.strip().upper()
                if alias:
                    mapping[alias] = row["entrez_id"]

    # -------- Previous symbols --------
    # Map historical gene names to current Entrez IDs
    if "prev_symbol" in hgnc.columns:
        prev_df = hgnc[["prev_symbol", "entrez_id"]].dropna()

        for _, row in prev_df.iterrows():
            for prev in str(row["prev_symbol"]).split("|"):
                prev = prev.strip().upper()
                if prev:
                    mapping[prev] = row["entrez_id"]

    print(f"Total HGNC mapping entries: {len(mapping)}")

    # =========================
    # APPLY MAPPING FUNCTION
    # =========================
    def apply_mapping(df, name):
        # Map Hugo_Symbol → Entrez Gene ID
        df["Entrez_Gene_Id"] = df["Hugo_Symbol"].map(mapping)

        before = len(df)

        # Remove rows without valid mapping
        df = df[df["Entrez_Gene_Id"].notna()]

        after = len(df)

        print(f"{name}: kept {after} of {before} rows after HGNC mapping.")

        return df

    # Apply mapping to each dataset
    expr = apply_mapping(expr, "Expression")
    cna = apply_mapping(cna, "CNA")
    mut = apply_mapping(mut, "Mutation")

    # =========================
    # SAVE OUTPUT FILES
    # =========================
    expr.to_csv(base / "expr_step3.csv", index=False)
    cna.to_csv(base / "cna_step3.csv", index=False)
    mut.to_excel(base / "mut_step3.xlsx", index=False)

    print("Step 3 complete. HGNC mapping finished.")


# =========================
# RUN SCRIPT
# =========================
if __name__ == "__main__":
    run()
