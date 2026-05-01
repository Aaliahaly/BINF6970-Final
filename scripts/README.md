# Scripts

This folder contains all Python scripts used to execute the full multi-omics data processing pipeline.

## Overview

The scripts follow a structured workflow from raw data processing to final dataset generation and validation. Each script represents a distinct stage and uses the output of the previous step.

The pipeline can be executed step-by-step or fully using a single script.

---

## Pipeline Steps

1. Data cleaning  
2. Data validation  
3. Sample-level harmonization  
4. Gene-level harmonization  
5. HGNC-based gene identifier mapping  
6. Final dataset integration  
7. Validation and reporting  

---

## Scripts and Their Roles

- clean_clinical_sample.py: Cleans and standardizes clinical and sample data  
- clean_cna.py: Transforms and cleans CNA data  
- clean_expression.py: Transforms and cleans gene expression data  
- clean_mutations.py: Cleans mutation data and computes VAF  
- validator.py: Validates datasets and checks required fields  
- sample_harmonization.py: Matches samples across all datasets  
- gene_harmonization.py: Matches genes across datasets  
- hgnc_mapping.py: Standardizes gene identifiers using HGNC reference  
- finalize.py: Produces final integrated datasets  
- report.py: Generates validation metrics and summary report  
- run_pipeline.py: Executes the entire pipeline in the correct order  

---

## How to Run

Run full pipeline:

python run_pipeline.py

Run step-by-step:

python clean_clinical_sample.py  
python clean_cna.py  
python clean_expression.py  
python clean_mutations.py  
python validator.py  
python sample_harmonization.py  
python gene_harmonization.py  
python hgnc_mapping.py  
python finalize.py  
python report.py  

---

## Input and Output

Input data is read from the `data/` folder.  
Each script writes its output to the corresponding step folder inside `data/`.  

Final datasets are stored in:
- `data/06_Final_Integrated_Data/`
- `data/07_Validation_Report/`

---

## Notes

- All scripts assume the folder structure defined in this repository  
- Large datasets may need to be downloaded separately  
- The HGNC reference file is required for gene mapping  

---

## Expected Result

After running the pipeline:

- Data is fully cleaned and validated  
- Samples and genes are harmonized across all datasets  
- Gene identifiers are standardized  
- Final datasets are ready for database integration  
- A validation report confirms data consistency and completeness  
