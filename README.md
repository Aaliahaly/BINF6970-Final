# Brain Lower Grade Glioma Multi-Omics Database

**TCGA PanCancer Atlas | Fully Reproducible | Gene-Centered Multi-Omics Database | MySQL + Neo4j**

---

## Overview

This project builds a fully reproducible, gene-centered multi-omics database for Brain Lower Grade Glioma (LGG) using TCGA PanCancer Atlas data.

Cancer multi-omics data are usually distributed across separate files. Clinical information, mutations, copy number alterations, mRNA expression, and derived clinical features often have different structures and identifiers. This makes integration difficult and forces researchers to spend significant time on preprocessing before they can ask biological questions.

This project solves that problem by converting selected TCGA LGG datasets into a clean, validated, harmonized, and database-ready system.

The central design rule is:

**Every molecular observation must map to both a gene and a sample.**

This rule ensures that mutation, CNA, and expression records can be integrated consistently and queried directly.

The final system supports:

- Relational database querying using MySQL
- Graph-based exploration using Neo4j
- Reproducible Python-based data processing
- Structured SQL database population
- Biological interpretation of key LGG-associated genes

---

## GitHub Repository

GitHub repository link:

```text
https://github.com/Aaliahaly/BINF6970-Final.git
```

---

## Core Contributions

- Built a gene-centered multi-omics database for TCGA LGG data.
- Integrated clinical, mutation, CNA, and mRNA expression datasets.
- Applied deterministic Python-based cleaning, validation, and harmonization.
- Standardized sample identifiers and gene identifiers across all omics layers.
- Used HGNC mapping to resolve gene symbol inconsistencies.
- Designed a relational database schema normalized up to Fifth Normal Form.
- Generated SQL scripts for database creation and population.
- Built a populated MySQL database inside a virtual machine.
- Created SQL queries for retrieval, filtering, and biological analysis.
- Extended the analysis using Neo4j graph database modeling.
- Annotated key mutated genes using GeneCards, COSMIC, cBioPortal, OncoKB, and ClinVar.
- Documented the full workflow for reproducibility.

---

## System Architecture

### Data Flow

```text
Selected TCGA LGG Data
        ↓
Python Cleaning
        ↓
Validation
        ↓
Sample-Level Harmonization
        ↓
Gene-Level Harmonization
        ↓
HGNC Gene Mapping
        ↓
Final Harmonization of all Datasets
        ↓
MySQL Relational Database
        ↓
SQL Population Script
        ↓
SQL Queries
        ↓
Neo4j Graph Analysis
```

---

## Design Principle

The database follows a strict gene-sample mapping structure.

Each molecular record must connect to:

1. A valid `Sample_ID`
2. A valid `Gene_ID`

This design allows clinical, mutation, CNA, and expression data to connect through a consistent relational structure.

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

This reduces redundancy and preserves biological meaning.

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

---

## Repository Structure

```text
project_root/

├── data (Hosted on Figshare) /
│   ├── TCGA_LGG_Original_Source_Data/
│   ├── TCGA_LGG_Original_Unused_Source_Files/
│   ├── TCGA_LGG_Original_Used_Source_Files/
│   ├── TCGA_LGG_Python_Pipeline_Input_Files/
│   ├── 01_Cleaned_Data/
│   ├── 02_Validated_Data/
│   ├── 03_Sample_Harmonized_Data/
│   ├── 04_Gene_Harmonized_Data/
│   ├── 05_HGNC_Mapped_Data/
│   ├── 06_Final_Curated_Data/
│   └── 07_Validation_Report/
│   └── Neo4j_Graph_Database_Files/
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
├── sql (Hosted on Figshare)/
│   ├── 01_create_database_schema.sql
│   ├── 02_load_cleaned_data.sql
│   └── 03_mydump.sql
│
├── diagrams/
│   ├── conceptual_model.png
│   └── logical_model_erd.png
│
├── docs/
│   ├── final_project_writeup.pdf
│
├── .gitignore
└── README.md

```

---

## External Data Availability

Large project files are hosted externally on Figshare to keep the GitHub repository lightweight and reproducible.

| Dataset Stage | Figshare Dataset Title | Link |
|---|---|---|
| Original Full Source Data| `TCGA_LGG_Original_Source_Data` | https://doi.org/10.6084/m9.figshare.32190318|
| Original Unused Source Files| `TCGA_LGG_Original_Unused_Source_Files` | https://doi.org/10.6084/m9.figshare.32190459|
| Original Used Source Files| `TCGA_LGG_Original_Used_Source_Files` | https://doi.org/10.6084/m9.figshare.32190600|
| Python Pipeline Input Files | `TCGA_LGG_Python_Pipeline_Input_Files` | https://doi.org/10.6084/m9.figshare.32194455 |
| Cleaned Data | `01_Cleaned_Data` | https://doi.org/10.6084/m9.figshare.32194497 |
| Validated Data | `02_Validated_Data` | https://doi.org/10.6084/m9.figshare.32194545 |
| Sample-Harmonized Data | `03_Sample_Harmonized_Data` | https://doi.org/10.6084/m9.figshare.32194617 |
| Gene-Harmonized Data | `04_Gene_Harmonized_Data` | https://doi.org/10.6084/m9.figshare.32194650 |
| HGNC-Mapped Data | `05_HGNC_Mapped_Data` | https://doi.org/10.6084/m9.figshare.32194674 |
| Final Harmonized Data | `06_Final_Harmonized_Data` | https://doi.org/10.6084/m9.figshare.32194689 |
| Final Proof Report | `07_Validation_Report` | https://doi.org/10.6084/m9.figshare.32194704 |
| SQL Database Files | `SQL_database_files` | https://doi.org/10.6084/m9.figshare.32204706 |
| Graph Database Files | `Neo4j_Graph_Database_Files` | https://doi.org/10.6084/m9.figshare.32206935 |

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

Files that did not fit the gene-centered design were excluded, including arm-level CNA, segment-level CNA, methylation, proteomics, structural variants, timeline files, resource files, case list files, and metadata files.

---

## Python Pipeline

The Python pipeline performs data cleaning, validation, harmonization, and final proof reporting.

Steps 1 to 7 can be run together using:

```bash
python run_pipeline.py
```

---

## Pipeline Steps

### 1. Data Cleaning

The cleaning stage prepares the clinical, sample, mutation, CNA, and expression datasets.

#### Clinical and Sample Cleaning

Python file:

```text
01_clean_clinical_sample.py
```

Main tasks:

- Standardizes clinical and sample column names.
- Renames survival variables.
- Converts survival status codes into readable labels.
- Rounds survival time variables.
- Standardizes cancer type and cancer site.
- Extracts IDH status and 1p/19q codeletion status.
- Produces a clean clinical and sample dataset.

#### CNA Transformation and Cleaning

Python file:

```text
02_clean_cna.py
```

Main tasks:

- Converts CNA data from wide format to long format.
- Creates one row per gene-sample pair.
- Stores numeric copy number values in `CNA_Value`.
- Maps numeric CNA values into biological categories in `CNA_Status`.

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
03_clean_expression.py
```

Main tasks:

- Converts mRNA expression data from wide format to long format.
- Creates one row per gene-sample pair.
- Converts expression values to numeric format.
- Rounds expression values.
- Removes zero-expression records.
- Removes duplicate records.

#### Mutation Cleaning

Python file:

```text
04_clean_mutations.py
```

Main tasks:

- Standardizes mutation fields.
- Renames consequence and impact columns.
- Selects the most severe consequence using VEP severity ranking.
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
05_validator.py
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
06_sample_harmonization.py
```

Main tasks:

- Standardizes sample identifiers.
- Identifies samples shared across clinical, mutation, CNA, and expression datasets.
- Retains only matched samples.
- Produces sample-harmonized files.

Outputs:

- `clin_step1.xlsx`
- `expr_step1.csv`
- `cna_step1.csv`
- `mut_step1.xlsx`

---

### 4. Gene-Level Harmonization

Python file:

```text
07_gene_harmonization.py
```

Main tasks:

- Standardizes gene symbols.
- Identifies genes shared across mutation, CNA, and expression datasets.
- Retains only shared genes.
- Produces gene-harmonized molecular files.

Outputs:

- `expr_step2.csv`
- `cna_step2.csv`
- `mut_step2.xlsx`

---

### 5. HGNC-Based Gene Identifier Mapping

Python file:

```text
08_hgnc_mapping.py
```

Main tasks:

- Maps gene symbols to HGNC-approved symbols.
- Uses aliases and previous names to resolve inconsistencies.
- Updates Entrez Gene IDs where needed.
- Removes unmapped or invalid gene records.
- Produces standardized molecular datasets.

Outputs:

- `expr_step3.csv`
- `cna_step3.csv`
- `mut_step3.xlsx`

---

### 6. Final Integration

Python file:

```text
09_finalize.py
```

Main tasks:

- Performs final sample-level and gene-level alignment.
- Ensures that clinical, mutation, CNA, and expression files are fully matched.
- Produces final database-ready datasets.

Outputs:

- `clin_FINAL.xlsx`
- `mut_FINAL.xlsx`
- `cna_FINAL.csv`
- `expr_FINAL.csv`

---

### 7. Final Validation Report

Python file:

```text
10_report.py
```

Main tasks:

- Generates a final proof report.
- Confirms dataset counts.
- Confirms patient, sample, gene, mutation, CNA, and expression consistency.
- Verifies readiness for database population.

Output:

```text
final_proof_report.txt
```

---

## Final Dataset Summary

The final harmonized dataset contains:

| Metric | Count |
|---|---:|
| Patients | 499 |
| Samples | 499 |
| Diagnosis | 499 |
| Survival  | 499 |
| Genes | 12,311 |
| Mutations | 33,653 |
| Sample_Mutation | 34,282|
| Expression  | 5,514,987 |
| CNA  | 1,150,724 |
| Feature_Definition| 3 |
| Sample_Feature | 1497 |
---

## SQL Database Population

SQL population is performed after the Python pipeline.

This step is not part of `run_pipeline.py`.

Python file:

```text
SQL_generation_for_populating_the_data.py
```

Input files:

- `clin_FINAL.xlsx`
- `mut_FINAL.xlsx`
- `cna_FINAL.csv`
- `expr_FINAL.csv`

Output file:

```text
FINAL_POPULATE.sql
```

This script converts the final harmonized datasets into structured SQL `INSERT` statements.

It also:

- Standardizes inserted values.
- Maps relationships between patients, samples, genes, and mutations.
- Deduplicates records.
- Aligns records with database constraints.
- Produces a ready-to-run SQL population script.

In the SQL directory and Figshare archive, this file is documented as:

```text
02_load_cleaned_data.sql.zip
```

---

## MySQL Database Construction

The MySQL database is built and populated inside the virtual machine.

Database name:

```text
Database
```

### Build the database schema

```bash
mysql -u root -p < 01_create_database_schema.sql
```

### Populate the database

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

### Export the populated database as a MySQL dump

```bash
mysqldump --single-transaction -h 127.0.0.1 -P 3306 -u root -p Database > mydump.sql
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

---

## SQL Analysis

The database supports structured SQL queries for:

- Retrieving samples for selected patients.
- Counting mutation impact levels.
- Mapping mutated genes in selected samples.
- Retrieving CNA states by gene and sample.
- Retrieving survival outcomes.
- Filtering high-VAF mutations.
- Ranking samples by mutation burden.
- Retrieving hypoxia-related sample features.
- Identifying samples with gene amplifications.
- Connecting patients, samples, mutations, genes, and VAF values.
- Ranking the most frequently mutated genes.
- Identifying samples with high average VAF.
- Counting amplification burden.
- Ranking patients by survival time.

These queries demonstrate that the relational schema supports integrated clinical and molecular analysis.

---

## Neo4j Graph Database Analysis

Neo4j is used as an analytical extension, not as the primary storage system.

Python file:

```text
Neo4j.py
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

- `TP53`
- `ATRX`
- `CIC`
- `FUBP1`

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

The integrated database and graph analysis support known LGG subtype patterns:

- `TP53` and `ATRX` are enriched in IDH-mutant astrocytoma.
- `CIC` and `FUBP1` are enriched in IDH-mutant, 1p/19q-codeleted oligodendroglioma.
- `TP53` and `ATRX` tend to co-occur.
- `CIC` and `FUBP1` tend to co-occur.
- `TP53/ATRX` alterations are largely distinct from `CIC/FUBP1` and 1p/19q-codeleted tumors.

---

## Workflow - Detailed

The project workflow was carried out in four main stages.

### 1. Run Python data processing locally on the Mac

Steps 1 to 7 can be run together using:

```bash
python run_pipeline.py
```

This includes:

1. Data cleaning
2. Dataset validation
3. Sample harmonization
4. Gene harmonization
5. HGNC mapping
6. Final integration
7. Final validation report

### 2. Generate the SQL population script

Run separately after the main pipeline:

```bash
python SQL_generation_for_populating_the_data.py
```

### 3. Transfer SQL scripts to the virtual machine

The schema and population scripts are transferred to the virtual machine using the shared folder.

Example shared folder:

```text
/media/sf_DB-Final/
```

### 4. Build and populate the database inside the virtual machine

Run:

```bash
mysql -u root -p < 01_create_database_schema.sql
```

Then run:

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

### 5. Run SQL queries

SQL queries can be executed inside the virtual machine after the database is populated.

### 6. Perform optional Neo4j analysis

After exporting selected SQL query results into `For Neo4j.csv`, run:

```bash
python Neo4j.py
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
- Validation report
- Neo4j input and Cypher output files
- Documentation of all major processing decisions
- Clear execution steps

---

## Validation

The final project includes validation at multiple levels:

- Dataset-level validation
- Sample-level consistency checks
- Gene-level consistency checks
- HGNC identifier validation
- Final proof report
- Database population verification
- SQL query output verification
- Neo4j graph output verification

The final validation confirms consistency between the processed datasets and the populated database.

---

## Documentation

The documentation includes:

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

## Final Note

This project reduces one of the most time-consuming barriers in cancer bioinformatics:

**data preparation.**

The final system provides clean, integrated, validated, and biologically interpretable data that can be queried directly using MySQL and explored further using Neo4j.

