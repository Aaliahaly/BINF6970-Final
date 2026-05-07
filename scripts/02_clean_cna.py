"""
This script transforms copy number alteration data from a wide matrix format
into a normalized long-format table.

Each output row represents one unique gene-sample pair with its corresponding
numeric CNA value and biological CNA status.

What this script does:
- Reads the CNA input file from Desktop
- Standardizes gene identifiers
- Converts the CNA dataset from wide format to long format
- Stores numeric CNA values in CNA_Value
- Converts CNA values to numeric format
- Maps numeric CNA values to biological labels in CNA_Status
- Handles missing or invalid CNA values as "unknown"
- Removes exact duplicate rows
- Reports the number of removed duplicate rows
- Saves a clean CSV file for downstream database integration and analysis
"""

import pandas as pd
from pathlib import Path


# =========================
# 1. READ INPUT FILE
# =========================

# Define input file path
file_path = Path.home() / "Desktop" / "data_cna.txt"

# Read tab-separated CNA file
df = pd.read_csv(file_path, sep="\t")


# =========================
# 2. STANDARDIZE IDENTIFIERS
# =========================

# Convert Entrez Gene ID to nullable integer format
df["Entrez_Gene_Id"] = pd.to_numeric(
    df["Entrez_Gene_Id"],
    errors="coerce"
).astype("Int64")

# Convert Hugo gene symbol to string format
df["Hugo_Symbol"] = df["Hugo_Symbol"].astype(str)


# =========================
# 3. CONVERT WIDE FORMAT TO LONG FORMAT
# =========================

# Convert sample columns into rows
df_long = df.melt(
    id_vars=["Hugo_Symbol", "Entrez_Gene_Id"],
    var_name="Sample_ID",
    value_name="CNA_Value"
)


# =========================
# 4. CONVERT CNA VALUES TO NUMERIC
# =========================

# Convert CNA values to numeric format
# Invalid values become NaN
df_long["CNA_Value"] = pd.to_numeric(
    df_long["CNA_Value"],
    errors="coerce"
)


# =========================
# 5. CREATE BIOLOGICAL CNA STATUS LABELS
# =========================

def map_cna_status(value):
    """
    Convert numeric CNA values into biological CNA status labels.
    """

    if pd.isna(value):
        return "unknown"

    elif value == -2:
        return "deep_loss"

    elif value == -1:
        return "loss"

    elif value == 0:
        return "neutral"

    elif value == 1:
        return "gain"

    elif value == 2:
        return "amplification"

    else:
        return "unknown"


# Apply CNA status mapping
df_long["CNA_Status"] = df_long["CNA_Value"].apply(map_cna_status)


# =========================
# 6. REORDER COLUMNS
# =========================

df_long = df_long[
    [
        "Hugo_Symbol",
        "Entrez_Gene_Id",
        "Sample_ID",
        "CNA_Value",
        "CNA_Status"
    ]
]


# =========================
# 7. REMOVE EXACT DUPLICATES
# =========================

# Count rows before duplicate removal
before = len(df_long)

# Remove exact duplicate rows
df_long = df_long.drop_duplicates()

# Count rows after duplicate removal
after = len(df_long)

# Print duplicate removal summary
print("Number_of_CNA_Rows_Before_Duplicate_Removal:", before)
print("Number_of_CNA_Rows_After_Duplicate_Removal:", after)
print("Number_of_CNA_Rows_Removed:", before - after)


# =========================
# 8. SAVE OUTPUT FILE
# =========================

# Define output file path
output_path = Path.home() / "Desktop" / "cna_long.csv"

# Save clean CNA long-format table
df_long.to_csv(output_path, index=False)

# Confirmation message
print("CNA long-format table is ready.")
print("Output file saved to:", output_path)
