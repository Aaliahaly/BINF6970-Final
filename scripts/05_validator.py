'''
This script validates all input datasets before any processing step.

What it does:
- Ensures required columns exist (Sample_ID, Hugo_Symbol)
- Checks for missing or invalid identifiers
- Standardizes gene symbols (trim + uppercase)
- Removes empty or invalid gene entries
- Validates HGNC reference file structure
'''

import pandas as pd
from pathlib import Path

# Define base path (Desktop)
base = Path.home() / "Desktop"


def validate_dataset(df, name, check_gene=True):
    # =========================
    # CLEAN COLUMN NAMES
    # =========================
    # Remove hidden spaces from column names
    df.columns = df.columns.str.strip()

    # =========================
    # CHECK SAMPLE_ID
    # =========================
    # Ensure Sample_ID exists
    if "Sample_ID" not in df.columns:
        raise ValueError(f"{name} is missing the 'Sample_ID' column.")

    # Ensure no missing Sample_ID values
    if df["Sample_ID"].isna().any():
        raise ValueError(f"{name} contains missing values in 'Sample_ID'.")

    # =========================
    # CLEAN GENE SYMBOLS
    # =========================
    if check_gene:
        # Ensure Hugo_Symbol exists
        if "Hugo_Symbol" not in df.columns:
            raise ValueError(f"{name} is missing the 'Hugo_Symbol' column.")

        # Standardize gene symbols
        df["Hugo_Symbol"] = (
            df["Hugo_Symbol"]
            .astype(str)
            .str.strip()   # remove spaces
            .str.upper()   # enforce uppercase
        )

        # Remove invalid gene names
        df = df[df["Hugo_Symbol"] != ""]
        df = df[df["Hugo_Symbol"] != "NAN"]

    return df


def validate_hgnc():
    # =========================
    # CHECK FILE EXISTS
    # =========================
    hgnc_path = base / "hgnc_complete_set.txt"

    if not hgnc_path.exists():
        raise FileNotFoundError("HGNC file 'hgnc_complete_set.txt' was not found on Desktop.")

    # =========================
    # LOAD FILE
    # =========================
    hgnc = pd.read_csv(hgnc_path, sep="\t", low_memory=False)

    # Clean column names
    hgnc.columns = hgnc.columns.str.strip()

    # =========================
    # CHECK REQUIRED COLUMNS
    # =========================
    required_cols = ["symbol", "entrez_id"]

    for col in required_cols:
        if col not in hgnc.columns:
            raise ValueError(f"HGNC file is missing required column: {col}")

    # =========================
    # STANDARDIZE GENE SYMBOLS
    # =========================
    hgnc["symbol"] = hgnc["symbol"].astype(str).str.strip().str.upper()

    return hgnc
