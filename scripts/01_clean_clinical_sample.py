"""
This script cleans and standardizes a clinical dataset for downstream analysis.

What it does:
- Loads an Excel file from the Desktop
- Fixes column naming inconsistencies
- Standardizes survival status labels
- Rounds survival time variables
- Extracts molecular features (IDH + codeletion) from subtype
- Harmonizes cancer type and site naming
- Keeps only required columns in a strict order
- Saves a clean Excel file back to the Desktop
"""

import pandas as pd
from pathlib import Path

# =========================
# 1. LOAD FILE
# =========================
# Define base path (Desktop)
base = Path.home() / "Desktop"

# Define input file path
file_path = base / "Clinical&Sample(1).xlsx"

# Read Excel file into pandas DataFrame
df = pd.read_excel(file_path)

# Remove hidden spaces from column names (very common issue)
df.columns = df.columns.str.strip()


# =========================
# 2. RENAME COLUMNS
# =========================
# Standardize all column names to a clean, consistent schema
df = df.rename(columns={
    "PATIENT_ID": "Patient_ID",
    "SAMPLE_ID": "Sample_ID",
    "SEX": "Gender",
    "GENETIC_ANCESTRY_LABEL": "Genetic_Ancestry_Label",
    "OS_STATUS": "Overall_Survival_Status",
    "OS_MONTHS": "Overall_Survival_Months",
    "DSS_STATUS": "Disease_Specific_Survival_Status",
    "DSS_MONTHS": "Disease_Specific_Survival_Months",
    "DFS_STATUS": "Disease_Free_Status",
    "DFS_MONTHS": "Disease_Free_Months",
    "PFS_STATUS": "Progression_Free_Status",
    "PFS_MONTHS": "Progression_Free_Months",
    "AGE": "Diagnosis_Age",
    "TUMOR_TISSUE_SITE": "Cancer_Site",
    "CANCER_TYPE_ACRONYM": "Cancer_Type",
    "CANCER_TYPE_DETAILED": "Cancer_Histological_Type",
    "GRADE": "Tumor_Histologic_Grade",
    "ANEUPLOIDY_SCORE": "Aneuploidy_Score",
    "SAMPLE_TYPE": "Sample_Type",
    "SOMATIC_STATUS": "Somatic_Status",
    "BUFFA_HYPOXIA_SCORE": "Buffa_Hypoxia_Score",
    "WINTER_HYPOXIA_SCORE": "Winter_Hypoxia_Score",
    "RAGNUM_HYPOXIA_SCORE": "Ragnum_Hypoxia_Score"
})


# =========================
# 3. FIX Cancer_Type
# =========================
# Replace abbreviations with full descriptive names
if "Cancer_Type" in df.columns:
    df["Cancer_Type"] = df["Cancer_Type"].replace("LGG", "Low-Grade Glioma")


# =========================
# 4. SAFE STATUS CLEANING
# =========================
# Function to clean survival status fields safely
def fix_status(x):
    # Keep missing values unchanged
    if pd.isna(x):
        return x

    # Convert to string and remove extra spaces
    x = str(x).strip()

    # Define acceptable standard values
    valid_values = [
        "living", "deceased",
        "alive or dead tumor free", "dead with tumor",
        "disease free", "recurred or progressed",
        "censored", "disease progression"
    ]

    # If already clean → keep as is
    if x.lower() in valid_values:
        return x

    # Handle encoded format like "0:LIVING"
    if ":" in x:
        return x.split(":")[1].capitalize()

    # Otherwise → keep original value (no data loss)
    return x


# List of survival status columns to clean
status_cols = [
    "Overall_Survival_Status",
    "Disease_Specific_Survival_Status",
    "Disease_Free_Status",
    "Progression_Free_Status"
]

# Apply cleaning function to each column
for col in status_cols:
    if col in df.columns:
        print(f"Before cleaning {col}:", df[col].dropna().unique()[:3])
        df[col] = df[col].apply(fix_status)
        print(f"After cleaning {col}:", df[col].dropna().unique()[:3])


# =========================
# 5. ROUND MONTHS SAFELY
# =========================
# Convert survival times to numeric and round to 2 decimal places
month_cols = [
    "Overall_Survival_Months",
    "Disease_Specific_Survival_Months",
    "Disease_Free_Months",
    "Progression_Free_Months"
]

for col in month_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(2)


# =========================
# 6. FIX Cancer_Site
# =========================
# Standardize anatomical site naming
if "Cancer_Site" in df.columns:
    df["Cancer_Site"] = df["Cancer_Site"].replace("CNS", "Brain")


# =========================
# 7. CREATE IDH & CODELETION
# =========================
# Extract IDH mutation status from subtype text
def extract_idh(x):
    if pd.isna(x):
        return None
    x = str(x)
    if "IDHmut" in x:
        return "Mutant"
    elif "IDHwt" in x:
        return "Wildtype"
    return None


# Extract 1p/19q codeletion status
def extract_codeletion(x):
    if pd.isna(x):
        return None
    x = str(x)
    if "codel" in x:
        return "Codeleted"
    elif "non-codel" in x:
        return "Non-Codeleted"
    return None


# Apply extraction only if Subtype column exists
if "Subtype" in df.columns:
    df["IDH_Status"] = df["Subtype"].apply(extract_idh)
    df["Codeletion_Status"] = df["Subtype"].apply(extract_codeletion)


# =========================
# 8. KEEP FINAL COLUMNS
# =========================
# Define final schema (order matters for downstream tools like cBioPortal)
final_columns = [
    "Patient_ID",
    "Sample_ID",
    "Gender",
    "Genetic_Ancestry_Label",
    "Overall_Survival_Status",
    "Overall_Survival_Months",
    "Disease_Specific_Survival_Status",
    "Disease_Specific_Survival_Months",
    "Disease_Free_Status",
    "Disease_Free_Months",
    "Progression_Free_Status",
    "Progression_Free_Months",
    "Diagnosis_Age",
    "Cancer_Site",
    "Cancer_Type",
    "Cancer_Histological_Type",
    "IDH_Status",
    "Codeletion_Status",
    "Tumor_Histologic_Grade",
    "Aneuploidy_Score",
    "Sample_Type",
    "Somatic_Status",
    "Buffa_Hypoxia_Score",
    "Winter_Hypoxia_Score",
    "Ragnum_Hypoxia_Score"
]

# Keep only existing columns (avoids errors if some are missing)
df = df[[col for col in final_columns if col in df.columns]]


# =========================
# 9. SAVE FILE
# =========================
# Define output path
output_path = base / "Clinical&Sample.xlsx"

# Save cleaned dataset
df.to_excel(output_path, index=False)

# Confirmation message
print("\nDone. File saved at:", output_path)
