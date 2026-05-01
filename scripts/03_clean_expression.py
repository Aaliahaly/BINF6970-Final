'''
This script processes RNA-seq gene expression data from wide format into a clean,
normalized long format where each row represents a gene–sample pair.

What this script does:
- Reads the raw RNA-seq file from Desktop
- Standardizes gene identifiers (Entrez ID and gene symbol)
- Converts wide matrix into long format (one row per gene–sample pair)
- Cleans expression values and enforces numeric format
- Rounds values to reduce noise and file size
- Removes zero-expression rows to improve efficiency
- Removes duplicate rows to ensure data integrity
- Saves a structured file ready for downstream analysis and integration
'''

import pandas as pd
from pathlib import Path

# =========================
# 1. READ FILE
# =========================
# Define input file path
file_path = Path.home() / "Desktop" / "data_mrna_seq_v2_rsem.txt"

# Load tab-separated RNA-seq data
df = pd.read_csv(file_path, sep="\t")


# =========================
# 2. FIX TYPES
# =========================
# Convert Entrez Gene ID to numeric (nullable integer)
df["Entrez_Gene_Id"] = pd.to_numeric(df["Entrez_Gene_Id"], errors="coerce").astype("Int64")

# Ensure gene symbols are treated as strings
df["Hugo_Symbol"] = df["Hugo_Symbol"].astype(str)


# =========================
# 3. MELT (WIDE → LONG)
# =========================
# Convert wide matrix into long format:
# Each row = one gene–sample pair
df_long = df.melt(
    id_vars=["Hugo_Symbol", "Entrez_Gene_Id"],  # identifiers
    var_name="Sample_ID",                      # sample column
    value_name="Expression"                    # expression value
)


# =========================
# 4. CLEAN DATA
# =========================
# Convert expression values to numeric
df_long["Expression"] = pd.to_numeric(df_long["Expression"], errors="coerce")

# Round values to 2 decimal places (standardization + smaller file size)
df_long["Expression"] = df_long["Expression"].round(2)

# Remove rows with zero expression (non-informative)
df_long = df_long[df_long["Expression"] != 0]

# Remove exact duplicate rows
before = len(df_long)
df_long = df_long.drop_duplicates()
after = len(df_long)

# Report how many rows were removed
print("Number_of_Expression_Rows_Removed:", before - after)


# =========================
# 5. SAVE OUTPUT
# =========================
# Define output path
output_path = Path.home() / "Desktop" / "long_expression.csv"

# Save cleaned dataset
df_long.to_csv(output_path, index=False)

print("Done. File Saved.")
