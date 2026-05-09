# Brain Lower Grade Glioma Multi-Omics Database

**TCGA PanCancer Atlas | Fully Reproducible | Gene-Centered Multi-Omics Database | MySQL + Neo4j**

---

## Overview

This project builds a fully reproducible, gene-centered multi-omics database for Brain Lower Grade Glioma (LGG) using TCGA PanCancer Atlas data.

Cancer multi-omics data are commonly distributed across separate files. Clinical information, mutation records, copy number alteration data, mRNA expression matrices, and derived clinical features often use different structures, identifiers, and formats. This makes integration difficult and forces researchers to spend substantial time on data preprocessing before biological questions can be addressed.

This project solves that problem by converting selected TCGA LGG datasets into a clean, validated, harmonized, and database-ready system.

The central design rule is:

```text
Every molecular observation must map to both a gene and a sample.
```

This rule ensures that mutation, CNA, and expression records can be integrated consistently and queried directly.

The final system supports:

- Relational database querying using MySQL
- Graph-based exploration using Neo4j
- Reproducible Python-based data cleaning and harmonization
- Structured SQL database construction and population
- Biological interpretation of key LGG-associated genes

---

## GitHub Repository

```text
https://github.com/Aaliahaly/BINF6970-Final.git
```

---

## Core Contributions

- Built a gene-centered multi-omics database for TCGA LGG data.
- Integrated clinical, mutation, CNA, mRNA expression, and hypoxia-derived sample features.
- Applied deterministic Python-based cleaning, validation, and harmonization.
- Standardized sample identifiers and gene identifiers across all omics layers.
- Used HGNC mapping to resolve gene symbol inconsistencies.
- Designed a relational database schema normalized up to Fifth Normal Form.
- Generated SQL scripts for database schema creation and data population.
- Built and populated a MySQL database inside a virtual machine.
- Created SQL queries for retrieval, filtering, validation, and biological analysis.
- Extended the analysis using Neo4j graph database modeling.
- Annotated key mutated genes using GeneCards, COSMIC, cBioPortal, OncoKB, and ClinVar.
- Documented the full workflow for reproducibility.

---

## System Architecture

```text
Selected TCGA LGG Source Data
        ↓
Python Data Cleaning
        ↓
Dataset Validation
        ↓
Sample-Level Harmonization
        ↓
Gene-Level Harmonization
        ↓
HGNC-Based Gene Mapping
        ↓
Final Harmonized Database-Ready Datasets
        ↓
SQL Population Script Generation
        ↓
MySQL Database Construction and Population
        ↓
SQL Querying and Relational Analysis
        ↓
Optional Neo4j Graph-Based Analysis
```

---

## Tools and Technologies

| Category | Tools |
|---|---|
| Data source | TCGA PanCancer Atlas through cBioPortal |
| Programming language | Python |
| Python libraries | pandas, NumPy, openpyxl |
| Relational database | MySQL |
| Graph database | Neo4j |
| Gene reference | HGNC |
| External data hosting | Figshare |
| Development environment | Local Mac environment and virtual machine for MySQL implementation |

---

## Setup Requirements

To reproduce the project, the following tools are required:

- Python 3.13
- MySQL Server
- Neo4j Desktop or Neo4j Browser
- Required Python packages:

```text
pandas
numpy
openpyxl
```

Install the required Python packages using:

```bash
pip install pandas numpy openpyxl
```

Before running the pipeline, download the required Figshare datasets and place them in the corresponding local `data/` folders.

---

## Quick Start

Run the core Python pipeline from the project root directory:

```bash
python scripts/run_pipeline.py
```

Generate the SQL population script after the final harmonized datasets are available:

```bash
python scripts/SQL_generation_for_populating_the_data.py
```

Generate the Neo4j Cypher import script after the graph-ready CSV file is available:

```bash
python scripts/Neo4j.py
```

Build and populate the MySQL database using the SQL files documented in the `sql/` directory.

---

## Design Principle

The database follows a strict gene-sample mapping structure.

Each molecular record must connect to:

1. A valid `Sample_ID`
2. A valid `Gene_ID`

This design allows clinical, mutation, CNA, and expression data to connect through a consistent relational structure.

It also prevents ambiguous molecular records and supports reliable multi-omics querying.

---

## Database Design

The database was designed using a normalized relational model.

The major entities are:

- Patient
- Diagnosis
- Cancer
- Sample
- Gene
- Mutation
- Sample_Mutation
- Copy_Number_Alteration
- Expression
- Survival
- Feature_Definition
- Sample_Feature

The schema separates patient-level, diagnosis-level, sample-level, gene-level, and molecular-level information.

This structure reduces redundancy, preserves biological meaning, and supports future expansion.

---

## Normalization

The database schema is normalized up to Fifth Normal Form.

The normalization strategy ensures:

- Atomic attributes
- No repeating groups
- No partial dependencies
- No transitive dependencies
- Proper resolution of many-to-many relationships
- Strong referential integrity
- Minimal redundancy
- Clear separation between clinical and molecular entities

The `Sample_Mutation` table resolves the many-to-many relationship between samples and mutations.

The `Gene` table acts as a central reference entity for mutation, CNA, and expression records.

The `Feature_Definition` and `Sample_Feature` tables provide a flexible structure for derived sample-level features such as hypoxia scores.

---

## Repository Structure

```text
project_root/
├── data/
│   └── README.md
│
├── scripts/
│   ├── 01_clean_clinical_sample.py
│   ├── 02_clean_cna.py
│   ├── 03_clean_expression.py
│   ├── 04_clean_mutations.py
│   ├── 05_validator.py
│   ├── 06_sample_harmonization.py
│   ├── 07_gene_harmonization.py
│   ├── 08_hgnc_mapping.py
│   ├── 09_finalize.py
│   ├── 10_report.py
│   ├── run_pipeline.py
│   ├── SQL_generation_for_populating_the_data.py
│   └── Neo4j.py
│
├── sql/
│   └── README.md
│
├── diagrams/
│   ├── conceptual_model.png
│   └── logical_model_erd.png
│
├── docs/
│   ├── Final Project Writeup.pdf
│   └── README.md
│
├── .gitignore
└── README.md
```

Large datasets, SQL loading files, SQL dump files, and Neo4j graph files are hosted externally on Figshare. Their access links are provided in the `data/README.md` file and in the External Data Availability section below.

---

## External Data Availability

Large project files are hosted externally on Figshare to keep the GitHub repository lightweight and reproducible.

| Dataset Stage | Figshare Dataset Title | Link |
|---|---|---|
| Original Full Source Data | `TCGA_LGG_Original_Source_Data` | https://doi.org/10.6084/m9.figshare.32190318 |
| Original Unused Source Files | `TCGA_LGG_Original_Unused_Source_Files` | https://doi.org/10.6084/m9.figshare.32190459 |
| Original Used Source Files | `TCGA_LGG_Original_Used_Source_Files` | https://doi.org/10.6084/m9.figshare.32190600 |
| Python Pipeline Input Files | `TCGA_LGG_Python_Pipeline_Input_Files` | https://doi.org/10.6084/m9.figshare.32194455 |
| Cleaned Data | `01_Cleaned_Data` | https://doi.org/10.6084/m9.figshare.32194497 |
| Validated Data | `02_Validated_Data` | https://doi.org/10.6084/m9.figshare.32194545 |
| Sample-Harmonized Data | `03_Sample_Harmonized_Data` | https://doi.org/10.6084/m9.figshare.32194617 |
| Gene-Harmonized Data | `04_Gene_Harmonized_Data` | https://doi.org/10.6084/m9.figshare.32194650 |
| HGNC-Mapped Data | `05_HGNC_Mapped_Data` | https://doi.org/10.6084/m9.figshare.32194674 |
| Final Harmonized Data | `06_Final_Harmonized_Data` | https://doi.org/10.6084/m9.figshare.32194689 |
| Final Proof Report | `07_Validation_Report` | https://doi.org/10.6084/m9.figshare.32194704 |
| SQL Database Files | `SQL_database_files` | https://doi.org/10.6084/m9.figshare.32204706 |
| Neo4j Graph Database Files | `Neo4j_Graph_Database_Files` | https://doi.org/10.6084/m9.figshare.32206935 |

---

## Input Data

The project uses selected files from the TCGA LGG PanCancer Atlas dataset downloaded from cBioPortal.

The selected source files include:

- `data_clinical_patient.txt`
- `data_clinical_sample.txt`
- `data_clinical_supp_hypoxia.txt`
- `data_cna.txt`
- `data_mutations.txt`
- `data_mrna_seq_v2_rsem.txt`
- `hgnc_complete_set.txt`

Not all files from the original TCGA LGG download were used.

Files that did not fit the gene-centered design were excluded, including:

- Arm-level CNA files
- Segment-level CNA files
- Methylation files
- Proteomics files
- Structural variant files
- Treatment timeline files
- Sample acquisition timeline files
- Resource files
- Case list files
- Metadata files

These exclusions preserve a focused gene-centered structure based on records that can be linked directly to genes and samples.

---

## Python Data Cleaning and Harmonization Pipeline

The Python pipeline prepares the datasets for database construction.

It performs:

- Data cleaning
- Dataset validation
- Sample-level harmonization
- Gene-level harmonization
- HGNC-based gene identifier mapping
- Final harmonization
- Final validation reporting

The pipeline does not create or populate the MySQL database.

Database schema creation and database population are performed separately using SQL scripts after the final harmonized datasets are generated.

Run the data cleaning and harmonization pipeline from the project root directory:

```bash
python scripts/run_pipeline.py
```

---

## Pipeline Steps

### 1. Data Cleaning

The cleaning stage prepares the clinical, sample, mutation, CNA, and expression datasets.

#### Clinical and Sample Cleaning

Python file:

```text
scripts/01_clean_clinical_sample.py
```

Main tasks:

- Standardizes clinical and sample column names.
- Renames survival variables into readable clinical terms.
- Converts survival status codes into readable labels.
- Rounds survival time variables.
- Standardizes cancer type and cancer site.
- Extracts IDH status and 1p/19q codeletion status.
- Standardizes hypoxia score variables.
- Produces a clean clinical and sample dataset.

#### CNA Transformation and Cleaning

Python file:

```text
scripts/02_clean_cna.py
```

Main tasks:

- Converts CNA data from wide format to long format.
- Creates one row per gene-sample pair.
- Standardizes gene identifiers.
- Stores numeric copy number values in `CNA_Value`.
- Maps numeric CNA values into biological categories in `CNA_Status`.
- Removes duplicate records.

CNA status mapping:

```text
-2 = deep_loss
-1 = loss
 0 = neutral
 1 = gain
 2 = amplification
```

#### Gene Expression Transformation

Python file:

```text
scripts/03_clean_expression.py
```

Main tasks:

- Converts mRNA expression data from wide format to long format.
- Creates one row per gene-sample pair.
- Standardizes gene identifiers.
- Converts expression values to numeric format.
- Rounds expression values.
- Removes zero-expression records.
- Removes duplicate records.

#### Mutation Cleaning

Python file:

```text
scripts/04_clean_mutations.py
```

Main tasks:

- Standardizes mutation fields.
- Renames consequence and impact columns.
- Selects the most severe consequence using VEP severity ranking.
- Standardizes mutation annotation text.
- Converts read counts into numeric format.
- Calculates Variant Allele Frequency.

VAF formula:

```text
VAF = t_alt_count / (t_ref_count + t_alt_count)
```

---

### 2. Dataset Validation

Python file:

```text
scripts/05_validator.py
```

Main tasks:

- Checks required fields.
- Validates `Sample_ID`.
- Validates `Hugo_Symbol`.
- Removes invalid or inconsistent records.
- Confirms that cleaned files are ready for harmonization.
- Validates the HGNC reference file.

---

### 3. Sample-Level Harmonization

Python file:

```text
scripts/06_sample_harmonization.py
```

Main tasks:

- Standardizes sample identifiers.
- Identifies samples shared across clinical, mutation, CNA, and expression datasets.
- Retains only matched samples.
- Produces sample-harmonized files.

Outputs:

```text
clin_step1.xlsx
expr_step1.csv
cna_step1.csv
mut_step1.xlsx
```

---

### 4. Gene-Level Harmonization

Python file:

```text
scripts/07_gene_harmonization.py
```

Main tasks:

- Standardizes gene symbols.
- Identifies genes shared across mutation, CNA, and expression datasets.
- Retains only shared genes.
- Produces gene-harmonized molecular files.

Outputs:

```text
expr_step2.csv
cna_step2.csv
mut_step2.xlsx
```

---

### 5. HGNC-Based Gene Identifier Mapping

Python file:

```text
scripts/08_hgnc_mapping.py
```

Main tasks:

- Maps gene symbols to HGNC-approved symbols.
- Uses aliases and previous names to resolve inconsistencies.
- Updates Entrez Gene IDs where needed.
- Removes unmapped or invalid gene records.
- Produces standardized molecular datasets.

Outputs:

```text
expr_step3.csv
cna_step3.csv
mut_step3.xlsx
```

---

### 6. Final Harmonization

Python file:

```text
scripts/09_finalize.py
```

Main tasks:

- Performs final sample-level and gene-level alignment.
- Ensures that clinical, mutation, CNA, and expression files are fully matched.
- Produces final database-ready datasets.

Outputs:

```text
clin_FINAL.xlsx
mut_FINAL.xlsx
cna_FINAL.csv
expr_FINAL.csv
```

---

### 7. Final Validation Report

Python file:

```text
scripts/10_report.py
```

Main tasks:

- Generates a final proof-of-integrity report.
- Confirms dataset counts.
- Confirms patient, sample, gene, mutation, CNA, expression, and feature consistency.
- Verifies readiness for database population.

Output:

```text
final_proof_report.txt
```

---

## Final Dataset Summary

The final harmonized datasets contain:

| Metric | Count |
|---|---:|
| Patients | 499 |
| Samples | 499 |
| Diagnoses | 499 |
| Survival records | 499 |
| Genes | 12,311 |
| Mutations | 33,653 |
| Sample_Mutation records | 34,282 |
| Expression records | 5,514,987 |
| CNA records | 1,150,724 |
| Feature definitions | 3 |
| Sample feature records | 1,497 |

---

## SQL Population Script Generation

SQL population script generation is performed after the Python data cleaning and harmonization pipeline.

This step is not part of `run_pipeline.py`.

Python file:

```text
scripts/SQL_generation_for_populating_the_data.py
```

Input files:

```text
clin_FINAL.xlsx
mut_FINAL.xlsx
cna_FINAL.csv
expr_FINAL.csv
```

Output file:

```text
FINAL_POPULATE.sql
```

This script converts the final harmonized datasets into structured SQL `INSERT` statements.

It also:

- Standardizes inserted values.
- Maps relationships between patients, diagnoses, samples, genes, and mutations.
- Deduplicates records.
- Aligns records with database constraints.
- Produces a ready-to-run SQL population script.

In the SQL directory and Figshare archive, this file is provided as:

```text
02_load_cleaned_data.sql
```

Run the script from the project root directory:

```bash
python scripts/SQL_generation_for_populating_the_data.py
```

---

## MySQL Database Implementation

The MySQL database is implemented after the Python processing steps are completed.

This stage uses:

```text
01_create_database_schema.sql
02_load_cleaned_data.sql
03_mydump.sql
```

The schema file creates the database structure.

The loading file populates the database with the final harmonized data.

The dump file allows direct reconstruction of the populated database.

Database name used in this project:

```text
Database
```

### Option 1: Build and Populate the Database

Create the schema:

```bash
mysql -u root -p < 01_create_database_schema.sql
```

Populate the database:

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

### Option 2: Reconstruct the Populated Database from the Dump

Restore the populated database directly:

```bash
mysql -u root -p Database < 03_mydump.sql
```

### Export the Populated Database as a MySQL Dump

```bash
mysqldump --single-transaction -h 127.0.0.1 -P 3306 -u root -p Database > 03_mydump.sql
```

---

## SQL Files

| SQL File | Purpose |
|---|---|
| `01_create_database_schema.sql` | Creates the database schema, tables, keys, and relationships. |
| `02_load_cleaned_data.sql` | Loads the cleaned and harmonized data into the database. |
| `03_mydump.sql` | Reconstructs the populated database directly. |

SQL database files are hosted externally on Figshare:

```text
https://doi.org/10.6084/m9.figshare.32204706
```

Detailed SQL reconstruction instructions are provided in:

```text
sql/README.md
```

---

## SQL Analysis

The database supports structured SQL queries for:

- Retrieving samples for selected patients
- Counting mutation impact levels
- Mapping mutated genes in selected samples
- Retrieving CNA states by gene and sample
- Retrieving survival outcomes
- Filtering high-VAF mutations
- Ranking samples by mutation burden
- Retrieving hypoxia-related sample features
- Identifying samples with gene amplifications
- Connecting patients, samples, mutations, genes, and VAF values
- Ranking the most frequently mutated genes
- Identifying samples with high average VAF
- Counting amplification burden
- Ranking patients by survival time

These queries demonstrate that the relational schema supports integrated clinical and molecular analysis.

---

## Neo4j Graph Database Analysis

Neo4j is used as an analytical extension, not as the primary storage system.

Python file:

```text
scripts/Neo4j.py
```

Input file:

```text
For Neo4j.csv
```

Output file:

```text
neo4j_import.cypher
```

The Neo4j script:

- Generates Cypher queries.
- Creates sample nodes.
- Creates gene nodes.
- Assigns IDH status to sample nodes.
- Assigns 1p/19q codeletion status to sample nodes.
- Defines relationships between samples and genes.
- Supports network-based exploration of mutation patterns.

Graph database files are hosted externally on Figshare:

```text
https://doi.org/10.6084/m9.figshare.32206935
```

Run the script from the project root directory:

```bash
python scripts/Neo4j.py
```

---

## Neo4j Graph Structure

### Nodes

- Sample
- Gene

### Relationships

- `HAS_GENE`

### Sample Attributes

- `Sample_ID`
- `IDH_Status`
- `Codeletion_Status`

### Gene Attributes

- `Hugo_Symbol`

---

## Biological Analysis

The project focuses on key LGG-associated genes, including:

```text
TP53
ATRX
CIC
FUBP1
```

These genes were examined using major bioinformatics and cancer genomics databases, including:

- GeneCards
- COSMIC
- cBioPortal
- OncoKB
- ClinVar

The analysis captures:

- Gene function
- Variant patterns
- Clinical significance
- LGG population frequency
- Molecular subtype association
- TCGA LGG-specific biological notes

---

## Key Biological Findings

The observed patterns are consistent with known LGG molecular subtype biology.

Key findings include:

- `TP53` and `ATRX` alterations are associated with IDH-mutant astrocytoma patterns.
- `CIC` and `FUBP1` alterations are associated with IDH-mutant, 1p/19q-codeleted oligodendroglioma patterns.
- `TP53` and `ATRX` tend to co-occur.
- `CIC` and `FUBP1` tend to co-occur.
- `TP53/ATRX` alteration patterns are largely distinct from `CIC/FUBP1` and 1p/19q-codeleted tumor patterns.

---

## Detailed Reproduction Workflow

The project workflow is organized into six main stages.

### 1. Run Python Data Cleaning and Harmonization

Run from the project root directory:

```bash
python scripts/run_pipeline.py
```

This step performs:

1. Data cleaning
2. Dataset validation
3. Sample-level harmonization
4. Gene-level harmonization
5. HGNC-based gene identifier mapping
6. Final harmonization
7. Final validation reporting

This step produces the final harmonized datasets needed for database construction.

It does not create the MySQL database and does not populate the database.

---

### 2. Generate the SQL Population Script

Run separately after the main pipeline:

```bash
python scripts/SQL_generation_for_populating_the_data.py
```

This step generates the SQL insert script used to populate the MySQL database.

---

### 3. Transfer SQL Scripts to the Virtual Machine

The schema and population scripts can be transferred to the virtual machine using the shared folder.

Example shared folder:

```text
/media/sf_DB-Final/
```

---

### 4. Build and Populate the Database Inside the Virtual Machine

Build the schema:

```bash
mysql -u root -p < 01_create_database_schema.sql
```

Populate the database:

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

Export the populated database:

```bash
mysqldump --single-transaction -h 127.0.0.1 -P 3306 -u root -p Database > 03_mydump.sql
```

---

### 5. Run SQL Queries

SQL queries can be executed inside the virtual machine after the database is populated.

The queries validate the relational structure and support integrated clinical-genomic analysis.

---

### 6. Perform Optional Neo4j Analysis

After exporting selected SQL query results into `For Neo4j.csv`, run:

```bash
python scripts/Neo4j.py
```

Then import or execute the generated Cypher script in Neo4j:

```text
neo4j_import.cypher
```

---

## Reproducibility

The project is reproducible because it includes:

- Selected input files
- Python scripts
- SQL schema file
- SQL population file
- SQL dump file
- Final harmonized datasets
- Final validation report
- Neo4j input and Cypher output files
- Documentation of major processing decisions
- Clear execution steps
- External Figshare archives for large files

The workflow separates data processing, SQL generation, database implementation, SQL analysis, and graph analysis into distinct steps.

This makes the project easier to reproduce, inspect, debug, and extend.

---

## Validation

The final project includes validation at multiple levels:

- Dataset-level validation
- Sample-level consistency checks
- Gene-level consistency checks
- HGNC identifier validation
- Final proof-of-integrity report
- Database population verification
- SQL query output verification
- Neo4j graph output verification

The final validation confirms consistency between the processed datasets and the populated database.

The validation report confirms the final counts for patients, samples, genes, mutations, expression records, CNA records, and sample features.

---

## Documentation

The final project writeup is located in:

```text
docs/Final Project Writeup.pdf
```

The writeup includes:

- Project overview
- Data source screening table
- Entity-relationship diagram
- Normalization explanation
- Data dictionary
- Python script map
- SQL queries with rationale and outputs
- Neo4j graph analysis
- Biological gene annotation table
- Reproduction steps
- Limitations and future work

Additional README files are provided in:

```text
data/README.md
scripts/README.md
sql/README.md
docs/README.md
```

---

## Limitations

This project has several limitations:

- It focuses on one cancer type: Brain Lower Grade Glioma.
- It uses selected TCGA PanCancer Atlas data.
- It does not include methylation, proteomics, structural variants, or treatment timeline data.
- Neo4j is used for graph-based analysis only, not full database storage.
- The current workflow uses static processed datasets rather than live database updates.
- Treatment-response and longitudinal clinical modeling are outside the current scope.

---

## Future Work

Future development could include:

- Adding methylation data.
- Adding proteomics data.
- Adding structural variant data.
- Extending the database to other cancer types.
- Adding treatment and longitudinal clinical data.
- Building automated dashboards.
- Adding machine learning workflows.
- Creating dynamic feature extraction tools.
- Expanding Neo4j graph modeling to include more molecular relationships.

---

## Project Significance

This project converts fragmented TCGA LGG multi-omics files into a clean, validated, gene-centered, and query-ready database system.

It reduces one of the most time-consuming barriers in cancer bioinformatics: data preparation.

The final system allows users to move directly into clinical-genomic analysis using MySQL, with Neo4j available as an additional graph-based exploration layer.
