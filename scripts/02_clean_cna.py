'''
This script transforms copy number alteration data from a wide matrix into a normalized ...
long format where each row represents a unique gene–sample pair with its corresponding CNA value.

What this script does:
- Reads the CNA input file from Desktop
- Ensures consistent data types for gene identifiers
- Converts wide matrix (samples as columns) into long format (one row per gene–sample pair)
- Converts CNA values into numeric format
- Maps numeric CNA values to biologically meaningful labels
- Handles missing values explicitly as "unknown"
- Removes exact duplicate rows while preserving original structure
- Saves a clean CSV file ready for downstream integration and analysis
'''

import pandas as pd
from pathlib import Path

# =========================
# 1. READ FILE
# =========================
# Define file path (Desktop)
file_path = Path.home() / "Desktop" / "data_cna.txt"

# Read tab-separated CNA file into DataFrame
df = pd.read_csv(file_path, sep="\t")

# Ensure Entrez Gene IDs are numeric (nullable integer type)
df["Entrez_Gene_Id"] = pd.to_numeric(df["Entrez_Gene_Id"], errors="coerce").astype("Int64")

# Ensure gene symbols are treated as strings
df["Hugo_Symbol"] = df["Hugo_Symbol"].astype(str)


# =========================
# 2. MELT (WIDE → LONG)
# =========================
# Convert wide matrix into long format:
# Each row will represent one gene–sample pair
df_long = df.melt(
    id_vars=["Hugo_Symbol", "Entrez_Gene_Id"],  # columns to keep fixed
    var_name="Sample_ID",                      # new column for sample names
    value_name="CNA_Status"                    # new column for CNA values
)


# =========================
# 3. ENSURE NUMERIC
# =========================
# Convert CNA values to numeric format (invalid values become NaN)
df_long["CNA_Status"] = pd.to_numeric(df_long["CNA_Status"], errors="coerce")


# =========================
# 4. CREATE LABELS
# =========================
# Map numeric CNA values to biological interpretation
def cna_label(x):
    if pd.isna(x):
        return "unknown"          # Missing or invalid values
    elif x == -2:
        return "deep_loss"        # Homozygous deletion
    elif x == -1:
        return "loss"             # Single copy loss
    elif x == 0:
        return "neutral"          # Normal copy number
    elif x == 1:
        return "gain"             # Low-level gain
    elif x == 2:
        return "amplification"    # High-level amplification

# Apply labeling function
df_long["CNA_Label"] = df_long["CNA_Status"].apply(cna_label)


# =========================
# 5. REMOVE DUPLICATES
# =========================
# Count rows before duplicate removal
before = len(df_long)

# Remove exact duplicate rows
df_long = df_long.drop_duplicates()

# Count rows after cleaning
after = len(df_long)

# Print how many rows were removed
print("Number_of_CNA_Rows_Removed:", before - after)


# =========================
# 6. SAVE OUTPUT
# =========================
# Define output file path
output_path = Path.home() / "Desktop" / "cna_long.csv"

# Save cleaned long-format table
df_long.to_csv(output_path, index=False)

# Confirmation message
print("CNA long table ready.")
