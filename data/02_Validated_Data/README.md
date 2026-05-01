# Validated Data

This folder contains datasets after the validation stage of the pipeline.

## Description
At this stage, all cleaned datasets are systematically checked to ensure structural integrity, consistency, and readiness for downstream harmonization. The validation process enforces the presence of key identifiers, standardizes gene symbols, and removes invalid or inconsistent entries.

All input datasets used in this stage are sourced from the `01_Cleaned_Data/` folder.

## Purpose
The goal of this step is to guarantee that only high-quality, consistent, and reliable data proceeds to the harmonization stages. This prevents downstream errors and ensures accurate multi-omics integration.

## Validation Checks Performed

- Verified the presence of required fields such as:
  - `Sample_ID`
  - `Hugo_Symbol`
- Checked for missing, null, or invalid identifiers
- Standardized gene symbol formatting
- Removed empty or invalid rows
- Ensured consistent data types across key columns
- Validated the structure and required columns of the HGNC reference file (`hgnc_complete_set.txt`)

## Input Datasets

- Clinical&Sample.xlsx  
- long_expression.csv  
- Mutation.xlsx  
- cna_long.csv  
- hgnc_complete_set.txt  

## Output

Validated datasets with:
- consistent identifiers  
- no missing critical fields  
- standardized gene symbols  
- clean structure ready for harmonization  

## Script

This step is performed using:

validator.py

The script is located in the `scripts/` directory.

## Role in Pipeline

These validated datasets serve as input for:

- sample-level harmonization (`Step1_samples.py`)  
- gene-level harmonization (`Step2_genes.py`)  

## Note

This stage does not modify the biological meaning of the data. It focuses strictly on structural validation and data integrity to ensure that all subsequent processing steps operate on clean and consistent inputs.
