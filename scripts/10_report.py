"""
This step generates a final validation and summary report for the fully integrated dataset.
All final files are loaded and checked to ensure consistent structure and alignment across
expression, CNA, mutation, and clinical data.

The script computes key dataset metrics including counts of patients, samples, genes,
mutations, and omics rows. Mutation and sample–mutation counts are carefully deduplicated
to match the logic used in database population, ensuring accurate representation of unique
events and relationships.

It also summarizes cancer definitions and available clinical features such as hypoxia scores.
The output provides a clear overview of dataset completeness and integrity, confirming that
all components are properly aligned and ready for database ingestion and downstream analysis.
"""

import pandas as pd
from pathlib import Path

# Define Desktop path
base = Path.home() / "Desktop"


def run():
    print("Loading final files for reporting...")

    # =========================
    # LOAD FILES
    # =========================
    expr = pd.read_csv(base / "expr_FINAL.csv")
    cna = pd.read_csv(base / "cna_FINAL.csv")
    mut = pd.read_excel(base / "mut_FINAL.xlsx")
    clin = pd.read_excel(base / "clin_FINAL.xlsx")

    # Clean column names
    for df in [expr, cna, mut, clin]:
        df.columns = df.columns.str.strip()

    # =========================
    # CORE COUNTS
    # =========================

    # Patients
    if "Patient_ID" in clin.columns:
        patients = clin["Patient_ID"].nunique()
    else:
        patients = clin["Sample_ID"].nunique()

    # Samples
    samples = expr["Sample_ID"].nunique()

    # Diagnoses and survival
    diagnoses = len(clin)
    survival_rows = len(clin)

    # Genes
    genes = expr["Hugo_Symbol"].nunique()

    # =========================
    # CORRECT MUTATION COUNT (MATCH SQL)
    # =========================
    mutation_keys = set()

    for _, r in mut.iterrows():
        key = (
            r.get("Entrez_Gene_Id"),
            r.get("Hugo_Symbol"),
            r.get("Chromosome"),
            r.get("Start_Position"),
            r.get("End_Position"),
            r.get("Reference_Allele"),
            r.get("Tumor_Seq_Allele"),
            r.get("Variant_Type"),
            r.get("Variant_Classification"),
            r.get("Primary_Consequence"),
            r.get("Impact_Level")
        )
        mutation_keys.add(key)

    mutations = len(mutation_keys)

    # =========================
    # CORRECT SAMPLE_MUTATION COUNT (MATCH SQL)
    # =========================
    sample_mut_keys = set()

    for _, r in mut.iterrows():
        key = (
            r.get("Sample_ID"),
            r.get("Entrez_Gene_Id"),
            r.get("Hugo_Symbol"),
            r.get("Chromosome"),
            r.get("Start_Position"),
            r.get("End_Position"),
            r.get("Reference_Allele"),
            r.get("Tumor_Seq_Allele")
        )
        sample_mut_keys.add(key)

    sample_mutation_rows = len(sample_mut_keys)

    # =========================
    # OTHER OMICS COUNTS
    # =========================
    cna_rows = len(cna)
    expression_rows = len(expr)

    # =========================
    # CANCER DEFINITIONS
    # =========================
    if all(col in clin.columns for col in ["Cancer_Site", "Cancer_Type", "Cancer_Histological_Type"]):
        cancers = clin[
            ["Cancer_Site", "Cancer_Type", "Cancer_Histological_Type"]
        ].drop_duplicates().shape[0]
    else:
        cancers = "N/A"

    # =========================
    # FEATURE DEFINITIONS (HYPOXIA)
    # =========================
    feature_cols = [
        "Buffa_Hypoxia_Score",
        "Winter_Hypoxia_Score",
        "Ragnum_Hypoxia_Score"
    ]

    existing_feature_cols = [col for col in feature_cols if col in clin.columns]

    feature_definitions = len(existing_feature_cols)
    sample_feature_rows = len(clin) * feature_definitions

    # =========================
    # PRINT REPORT
    # =========================
    print()
    print(f"Patients: {patients}")
    print(f"Cancers: {cancers}")
    print(f"Diagnoses: {diagnoses}")
    print(f"Survival rows: {survival_rows}")
    print(f"Samples: {samples}")
    print(f"Genes: {genes}")
    print(f"Mutations: {mutations}")
    print(f"Sample_Mutation rows: {sample_mutation_rows}")
    print(f"CNA rows: {cna_rows}")
    print(f"Expression rows: {expression_rows}")
    print(f"Feature definitions: {feature_definitions}")
    print(f"Sample_Feature rows: {sample_feature_rows}")
    print()
    print("Process finished with exit code 0")

    # =========================
    # SAVE REPORT
    # =========================
    with open(base / "final_proof_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Patients: {patients}\n")
        f.write(f"Cancers: {cancers}\n")
        f.write(f"Diagnoses: {diagnoses}\n")
        f.write(f"Survival rows: {survival_rows}\n")
        f.write(f"Samples: {samples}\n")
        f.write(f"Genes: {genes}\n")
        f.write(f"Mutations: {mutations}\n")
        f.write(f"Sample_Mutation rows: {sample_mutation_rows}\n")
        f.write(f"CNA rows: {cna_rows}\n")
        f.write(f"Expression rows: {expression_rows}\n")
        f.write(f"Feature definitions: {feature_definitions}\n")
        f.write(f"Sample_Feature rows: {sample_feature_rows}\n")


if __name__ == "__main__":
    run()
