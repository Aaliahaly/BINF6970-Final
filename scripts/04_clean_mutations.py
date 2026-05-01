"""
This script selects the most severe consequence per mutation using
official VEP severity ranking.

What this script does:
- Loads mutation data from Excel
- Renames key columns for consistency with database schema
- Parses multiple consequence annotations per mutation
- Assigns a severity score using VEP ranking
- Keeps only the highest-impact consequence
- Standardizes mutation annotation fields
- Calculates Variant Allele Frequency (VAF)
- Outputs a clean, structured dataset ready for analysis
"""

import pandas as pd
from pathlib import Path

# =========================
# 1. LOAD FILE
# =========================
# Define base path (Desktop)
base = Path.home() / "Desktop"

# Define input file path
file_path = base / "Mutation(1).xlsx"

# Load Excel file into DataFrame
df = pd.read_excel(file_path)


# =========================
# 2. RENAME COLUMNS
# =========================
# Rename columns to match standardized database naming
df = df.rename(columns={
    "Consequence": "Primary_Consequence",   # raw consequence → processed primary consequence
    "IMPACT": "Impact_Level"                # impact → cleaner label
})


# =========================
# 3. VEP SEVERITY RANKING (HIGH → LOW)
# =========================
# Lower number = higher severity
severity_rank = {
    "transcript_ablation": 1,
    "splice_acceptor_variant": 2,
    "splice_donor_variant": 3,
    "stop_gained": 4,
    "frameshift_variant": 5,
    "stop_lost": 6,
    "start_lost": 7,
    "missense_variant": 8,
    "protein_altering_variant": 9,
    "inframe_insertion": 10,
    "inframe_deletion": 11,
    "synonymous_variant": 12,
    "intron_variant": 13,
    "upstream_gene_variant": 14,
    "downstream_gene_variant": 15,
    "intergenic_variant": 16
}


# =========================
# 4. FUNCTION TO PICK MOST SEVERE CONSEQUENCE
# =========================
def get_most_severe(consequence_string):
    # Handle missing values
    if pd.isna(consequence_string):
        return None

    # Split multiple consequences (comma-separated from VEP)
    consequences = str(consequence_string).lower().split(",")

    # Initialize best candidate
    best = None
    best_score = float("inf")

    # Loop through all consequences and pick the most severe
    for c in consequences:
        c = c.strip()
        score = severity_rank.get(c, 999)  # unknown terms get lowest priority

        if score < best_score:
            best_score = score
            best = c

    return best


# Apply severity selection to each row
df["Primary_Consequence"] = df["Primary_Consequence"].apply(get_most_severe)


# =========================
# 5. STANDARDIZE TEXT FORMAT
# =========================
# Normalize text fields (lower → Capitalized for consistency)
text_cols = [
    "Primary_Consequence",
    "Variant_Classification",
    "Variant_Type",
    "Impact_Level"
]

for col in text_cols:
    df[col] = df[col].astype(str).str.lower().str.capitalize()


# =========================
# 6. CALCULATE VARIANT ALLELE FREQUENCY (VAF)
# =========================
# Ensure read counts are numeric
df["t_ref_count"] = pd.to_numeric(df["t_ref_count"], errors="coerce")
df["t_alt_count"] = pd.to_numeric(df["t_alt_count"], errors="coerce")

# Compute VAF = alt / (ref + alt)
df["VAF"] = df["t_alt_count"] / (df["t_ref_count"] + df["t_alt_count"])

# Round VAF for consistency and readability
df["VAF"] = df["VAF"].round(2)


# =========================
# 7. FINAL COLUMN ORDER
# =========================
# Define strict schema for downstream database integration
final_columns = [
    "Sample_ID",
    "Hugo_Symbol",
    "Entrez_Gene_Id",
    "Chromosome",
    "Start_Position",
    "End_Position",
    "Primary_Consequence",
    "Variant_Classification",
    "Variant_Type",
    "Reference_Allele",
    "Tumor_Seq_Allele",
    "VAF",
    "Impact_Level"
]

# Keep only required columns (avoids unexpected fields)
df = df[final_columns]


# =========================
# 8. SAVE FILE
# =========================
# Define output file path
output_path = base / "Mutation.xlsx"

# Save cleaned mutation dataset
df.to_excel(output_path, index=False)

# Confirmation message
print("Done. File saved at:", output_path)
