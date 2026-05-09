# Scripts

This directory contains all Python scripts used to run the TCGA Lower Grade Glioma multi-omics data processing pipeline and the post-pipeline database implementation steps.

The scripts support the full workflow from selected TCGA LGG input files to cleaned, validated, harmonized, HGNC-mapped, final database-ready datasets, SQL population script generation, and Neo4j Cypher script generation.

Large input files, intermediate outputs, final outputs, SQL files, and Neo4j files are hosted externally on Figshare. The Figshare links are provided in the `README.md` file inside the `data/` directory.

---

## Overview

The project uses a structured Python pipeline to process TCGA Lower Grade Glioma multi-omics data.

The core pipeline performs:

1. Data cleaning and transformation
2. Dataset validation
3. Sample-level harmonization
4. Gene-level harmonization
5. HGNC-based gene identifier mapping
6. Final harmonization
7. Final proof-of-integrity report generation

The core pipeline can be executed automatically using:

```bash
python run_pipeline.py
```

or each script can be executed separately for inspection, debugging, and verification.

Two additional post-pipeline scripts are included:

1. `SQL_generation_for_populating_the_data.py`  
   Generates the SQL population script used to load the final harmonized datasets into the MySQL database.

2. `Neo4j.py`  
   Generates the Neo4j Cypher import script from a graph-ready CSV file prepared from SQL-based exploratory query outputs.

The SQL and Neo4j scripts are not part of `run_pipeline.py`. They are executed separately after the final harmonized datasets and graph-ready files are available.

---

## Script Inventory

| Script | Role |
|---|---|
| `01_clean_clinical_sample.py` | Cleans and standardizes clinical and sample data. |
| `02_clean_cna.py` | Transforms CNA data from wide format to long format and standardizes CNA values. |
| `03_clean_expression.py` | Transforms mRNA expression data from wide format to long format and cleans expression values. |
| `04_clean_mutations.py` | Cleans mutation data, standardizes annotations, selects the most severe consequence, and calculates Variant Allele Frequency. |
| `05_validator.py` | Validates cleaned datasets by checking required fields, identifiers, formats, and HGNC reference structure. |
| `06_sample_harmonization.py` | Harmonizes datasets at the sample level by retaining samples shared across clinical, expression, CNA, and mutation datasets. |
| `07_gene_harmonization.py` | Harmonizes molecular datasets at the gene level by retaining genes shared across expression, CNA, and mutation datasets. |
| `08_hgnc_mapping.py` | Standardizes gene identifiers using HGNC-approved symbols, aliases, previous gene names, and Entrez Gene IDs. |
| `09_finalize.py` | Performs final sample-level and gene-level alignment across all processed datasets. |
| `10_report.py` | Generates the final proof-of-integrity report with dataset metrics and integrity checks. |
| `run_pipeline.py` | Executes the core processing pipeline in the correct order. |
| `SQL_generation_for_populating_the_data.py` | Generates the SQL population script from the final harmonized datasets. |
| `Neo4j.py` | Generates the Neo4j Cypher import script from a graph-ready CSV file prepared from SQL-based exploratory query outputs. |

---

## Core Pipeline Execution

To run the full core pipeline, execute the following command from the project root directory:

```bash
python run_pipeline.py
```

This command runs the scripts in the correct order, from initial data cleaning to final proof-of-integrity reporting.

The full core pipeline includes:

1. Clinical and sample cleaning
2. CNA cleaning and transformation
3. mRNA expression cleaning and transformation
4. Mutation cleaning
5. Dataset validation
6. Sample-level harmonization
7. Gene-level harmonization
8. HGNC-based gene identifier mapping
9. Final harmonization
10. Final proof-of-integrity report generation

After successful execution, the pipeline generates the final database-ready datasets.

---

## Step-by-Step Core Pipeline Execution

The core pipeline scripts can also be run individually in the following order:

```bash
python 01_clean_clinical_sample.py
python 02_clean_cna.py
python 03_clean_expression.py
python 04_clean_mutations.py
python 05_validator.py
python 06_sample_harmonization.py
python 07_gene_harmonization.py
python 08_hgnc_mapping.py
python 09_finalize.py
python 10_report.py
```

This option is useful when reviewing intermediate outputs, checking the effect of each processing stage, or debugging errors.

---

## Post-Pipeline Script Execution

After the core pipeline has generated the final harmonized datasets, the database implementation scripts can be run separately.

These scripts support:

1. MySQL database population
2. Neo4j graph database population

---

## Generate the SQL Population Script

Use this script after the final harmonized datasets have been generated:

```bash
python SQL_generation_for_populating_the_data.py
```

This script uses the final harmonized datasets:

```text
clin_FINAL.xlsx
mut_FINAL.xlsx
cna_FINAL.csv
expr_FINAL.csv
```

It generates:

```text
FINAL_POPULATE.sql
```

The script originally generates `FINAL_POPULATE.sql`. For repository and Figshare documentation, this generated loading file is provided as:

```text
02_load_cleaned_data.sql
```

The generated SQL file contains structured `INSERT` statements used to populate the MySQL database.

This script maps and inserts records for:

- Patients
- Diagnoses
- Samples
- Genes
- Clinical records
- Mutation records
- Sample-mutation relationships
- Copy number alteration records
- mRNA expression records
- Survival records
- Sample-level molecular features

The script also standardizes inserted values, removes duplicate records, and preserves relationships required by the relational database schema.

---

## Generate the Neo4j Cypher Import Script

Use this script after the graph-ready CSV file has been prepared from SQL-based exploratory query outputs:

```bash
python Neo4j.py
```

This script uses:

```text
For Neo4j.csv
```

It generates:

```text
neo4j_import.cypher
```

The Neo4j script does not process the raw TCGA LGG multi-omics files directly.

Instead, it uses a graph-ready CSV file produced after SQL-based querying and filtering.

The generated Cypher file creates:

- Sample nodes
- Gene nodes
- IDH status attributes
- 1p/19q codeletion attributes
- Relationships between samples and genes

This script supports graph database population and network-based analysis in Neo4j.

---

## Data Availability

All large data files are hosted externally on Figshare.

This includes:

- Selected pipeline input files
- Cleaned datasets
- Validated datasets
- Sample-harmonized datasets
- Gene-harmonized datasets
- HGNC-mapped datasets
- Final harmonized datasets
- Final proof report
- SQL database files
- Neo4j graph database files

The repository does not store these large data files directly because some files exceed practical GitHub storage limits.

The Figshare links for all pipeline data stages are listed in:

```text
data/README.md
```

Before running the pipeline, download the required files from Figshare and place them in the corresponding folders inside the local `data/` directory.

---

## Input and Output Folder Structure

The pipeline reads input files from the project `data/` directory.

Each script writes its output to the corresponding stage-specific folder inside `data/`.

The expected folder structure is:

| Folder | Content |
|---|---|
| `data/Python_Pipeline_Input_Files/` | Selected input files used as the starting point for the Python pipeline. |
| `data/01_Cleaned_Data/` | Cleaned and transformed datasets. |
| `data/02_Validated_Data/` | Structurally validated datasets. |
| `data/03_Sample_Harmonized_Data/` | Sample-level harmonized datasets. |
| `data/04_Gene_Harmonized_Data/` | Gene-level harmonized datasets. |
| `data/05_HGNC_Mapped_Data/` | HGNC-mapped molecular datasets. |
| `data/06_Final_Harmonized_Data/` | Final harmonized database-ready datasets. |
| `data/07_Validation_Report/` | Final validation and proof-of-integrity report. |

These folders and their associated files are available through the Figshare links provided in `data/README.md`.

---

## Required Input Files for the Core Pipeline

The core pipeline starts from the selected Python pipeline input files.

Required files include:

```text
Clinical&Sample(1).xlsx
data_cna.txt
data_mrna_seq_v2_rsem.txt
Mutation(1).xlsx
hgnc_complete_set.txt
```

These files should be downloaded from the Figshare datasets listed in `data/README.md`.

The HGNC reference file is required for the gene identifier mapping stage.

---

## Required Files for SQL Population Script Generation

The SQL population script requires the final harmonized datasets:

```text
clin_FINAL.xlsx
mut_FINAL.xlsx
cna_FINAL.csv
expr_FINAL.csv
```

These files are generated by the core pipeline and are also available through the Figshare links listed in `data/README.md`.

Script:

```text
SQL_generation_for_populating_the_data.py
```

Generated output:

```text
FINAL_POPULATE.sql
```

Documented SQL loading file:

```text
02_load_cleaned_data.sql
```

---

## Required Files for Neo4j Script Generation

The Neo4j script requires the graph-ready CSV file:

```text
For Neo4j.csv
```

This file is prepared from SQL-based exploratory query outputs.

Script:

```text
Neo4j.py
```

Generated output:

```text
neo4j_import.cypher
```

The graph database files are hosted externally on Figshare and documented separately.

---

## Processing Workflow

The workflow begins with selected TCGA LGG pipeline input files.

The clinical and sample data are cleaned and standardized.

CNA and mRNA expression matrices are transformed from wide format into long format.

Mutation data are cleaned, standardized, and used to calculate Variant Allele Frequency.

After cleaning, the datasets are validated to confirm:

- Required identifiers
- Expected columns
- Consistent formatting
- Usable HGNC reference fields

The validated datasets are then harmonized at the sample level.

Only samples shared across clinical, expression, CNA, and mutation datasets are retained.

The molecular datasets are then harmonized at the gene level.

Only genes shared across expression, CNA, and mutation datasets are retained.

The gene identifiers are standardized using:

- HGNC-approved symbols
- HGNC aliases
- Previous gene names
- Entrez Gene IDs

The final harmonization step aligns all processed datasets across shared samples and shared standardized genes.

The final proof-of-integrity report summarizes dataset metrics and confirms that the outputs are complete, consistent, and ready for database construction.

After the core pipeline is complete, the SQL generation script converts the final harmonized datasets into a ready-to-run SQL population script.

After SQL querying, selected query outputs can be exported as `For Neo4j.csv`.

That CSV file is then used by `Neo4j.py` to generate the Cypher import script for Neo4j graph database analysis.

---

## Expected Final Outputs

After successful execution, the core pipeline generates the final harmonized datasets:

```text
expr_FINAL.csv
cna_FINAL.csv
mut_FINAL.xlsx
clin_FINAL.xlsx
```

The pipeline also generates the final proof-of-integrity report:

```text
final_proof_report.txt
```

The SQL generation script produces:

```text
FINAL_POPULATE.sql
```

The Neo4j script produces:

```text
neo4j_import.cypher
```

These outputs are ready for:

- SQL database population
- Relational querying
- Graph database construction
- Network-based analysis
- Downstream multi-omics interpretation

---

## Execution Summary

| Task | Command |
|---|---|
| Run full core pipeline | `python run_pipeline.py` |
| Generate SQL population script | `python SQL_generation_for_populating_the_data.py` |
| Generate Neo4j Cypher script | `python Neo4j.py` |

---

## Important Notes

The scripts assume that the repository folder structure has not been changed.

The core pipeline focuses on cleaning, standardization, validation, sample matching, gene matching, HGNC-based identifier mapping, and final database-ready formatting.

The core pipeline does not change the biological interpretation of the data.

`SQL_generation_for_populating_the_data.py` is executed separately after the final harmonized datasets are available.

`Neo4j.py` is executed separately after `For Neo4j.csv` has been generated from SQL-based exploratory outputs.

All large data files, intermediate datasets, final datasets, validation reports, SQL database files, and graph database files are stored on Figshare.

The data access links are provided in:

```text
data/README.md
```

and in the main project `README.md`.
