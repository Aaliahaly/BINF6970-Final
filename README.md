# Brain Lower Grade Glioma Multi-Omics Database  
**TCGA PanCancer Atlas | Fully Reproducible | Gene-Centered Data Architecture**

---

## Executive Overview

This project delivers a rigorously engineered, gene-centered multi-omics database for Brain Lower Grade Glioma (LGG) using TCGA PanCancer Atlas data.

Multi-omics datasets are inherently fragmented. Clinical data, mutations, copy number alterations, and gene expression exist in separate formats with inconsistent identifiers. This project resolves that fragmentation through a deterministic and fully reproducible pipeline that produces a clean, integrated, and query-ready system.

The core design rule is strict:

**Every molecular observation must map to both a gene and a sample.**

This guarantees consistency across all data layers and enables direct biological interpretation without additional preprocessing.

---

## Core Contributions

- End-to-end integration of clinical and multi-omics datasets  
- Strict gene–sample relational mapping  
- Schema normalized to Fifth Normal Form (5NF)  
- Fully reproducible pipeline for cleaning, validation, and harmonization  
- Automated SQL generation for database population  
- Dual analysis framework:
  - Relational querying (MySQL)
  - Graph-based exploration (Neo4j)  
- Quantitative validation of data integrity  

---

## System Architecture

### Data Flow

```
Raw Data → Cleaning → Validation → Harmonization → Integration → SQL → MySQL → Neo4j
```

### Design Principles

- Gene-centered structure  
- Strict normalization  
- Deterministic transformations  
- No redundancy  
- Scalable architecture  

---

## Repository Structure

```
project_root/

├── data/
│   ├── Original_TCGA_LGG_Dataset/
│   ├── Selected_Original_Files/
│   ├── Selected_Raw_Data/
│   ├── 01_Cleaned_Data/
│   ├── 02_Validated_Data/
│   ├── 03_Sample_Harmonized_Data/
│   ├── 04_Gene_Harmonized_Data/
│   ├── 05_HGNC_Mapped_Data/
│   ├── 06_Final_Curated_Data/
│   └── 07_Validation_Report/
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
│
├── sql/
│   ├── schema.sql
│   ├── FINAL_POPULATE.sql
│   └── queries.sql
│
├── diagrams/
│   ├── conceptual_model.png
│   └── logical_model_erd.png
│
├── docs/
│   ├── full_report
│   ├── data_dictionary
│   └── ERD
│
└── README.md
```

---

## Data Pipeline

### Stage 1: Cleaning

- Clinical standardization  
- Mutation processing with VAF calculation  
- CNA and expression reshaping to gene–sample format  

### Stage 2: Validation

- Required field enforcement  
- Removal of invalid records  

### Stage 3: Sample Harmonization

- Retain only samples present across all datasets  

### Stage 4: Gene Harmonization

- Retain only shared genes across all omics layers  

### Stage 5: HGNC Mapping

- Standardize gene identifiers  

### Stage 6: Final Integration

- Fully matched multi-omics dataset  

### Stage 7: Validation Report

Final dataset:

- Patients: 499  
- Samples: 499  
- Genes: 12,311  
- Mutations: 33,653  

---

## Important Note on Pipeline Execution

`run_pipeline.py` executes only:

- Sample harmonization  
- Gene harmonization  
- HGNC mapping  
- Final dataset integration  
- Validation reporting  

It does NOT perform initial data cleaning.

---

## Database Design

### Entities

- Patient  
- Diagnosis  
- Sample  
- Gene  
- Mutation  
- Copy_Number_Alteration  
- Expression  
- Survival  

### Key Properties

- Fully normalized to 5NF  
- No redundancy  
- Correct handling of many-to-many relationships  
- Strong referential integrity  
- Scalable structure aligned with clinical reality  

---

## SQL Analysis

Supports:

- Survival analysis  
- Mutation burden  
- Gene mutation frequency  
- Copy number analysis  
- High-VAF filtering  

All queries are efficient and scalable.

---

## Graph Analysis (Neo4j)

### Nodes

- Sample  
- Gene  

### Relationships

- HAS_GENE  

### Attributes

- IDH status  
- 1p/19q codeletion  

### Purpose

- Network-based mutation analysis  
- Subtype visualization  

Note: Neo4j is used for analysis, not full data storage.

---

## Biological Insights

- TP53 and ATRX enriched in IDH-mutant tumors  
- CIC and FUBP1 enriched in codeleted tumors  
- Strong subtype-specific mutation patterns  

---

## Reproducibility

### Environment Split

**Mac (Local):**
- Data cleaning  
- Validation  
- Harmonization  

**Virtual Machine:**
- Database creation  
- Data population  
- SQL queries  
- Neo4j analysis  

---

## Reproduction Steps

### 1. Run Pipeline (Local)

```bash
python run_pipeline.py
```

---

### 2. Transfer Data to Virtual Machine

Shared folder:

```
/media/sf_DB-Final/
```

---

### 3. Build Database

```bash
mysql -u root -p < schema.sql
```

---

### 4. Populate Database

```bash
mysql -u root -p < FINAL_POPULATE.sql
```

---

### 5. Run Queries

```bash
mysql < queries.sql
```

---

## Validation

- No duplicate records  
- No orphan relationships  
- Full consistency between pipeline output and database  
- Verified counts across all entities  

---

## Documentation

Located in `/docs/`:

- ERD  
- Data Dictionary  
- Full Report  
- Validation Results  

---

## Limitations and Future Work

- Single cancer type (LGG)  
- Limited omics layers (no methylation or proteomics)  
- Dependence on preprocessed data  
- Static derived metrics such as VAF  
- No treatment or longitudinal clinical data  

### Future Directions

- Add methylation and proteomics layers  
- Extend to multiple cancer types  
- Integrate treatment and time-series data  
- Enable dynamic feature computation  
- Incorporate machine learning workflows  

---

## Final Note

This system removes the most time-consuming barrier in cancer bioinformatics:

**data preparation.**

You work directly on clean, integrated, and biologically consistent data.

