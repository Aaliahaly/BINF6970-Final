# Brain Lower Grade Glioma Multi-Omics Database  
TCGA PanCancer Atlas | Fully Reproducible | SQL + Graph Integration

---

## 1. Executive Summary
This project delivers a rigorously engineered, gene-centered multi-omics database for Brain Lower Grade Glioma (LGG) using TCGA PanCancer Atlas data. The system resolves fragmentation across clinical, mutation, CNA, and expression datasets through a deterministic, reproducible pipeline.

Core contributions:
- End-to-end harmonization of multi-omics data at sample and gene levels
- Relational schema normalized to Fifth Normal Form (5NF)
- Automated pipeline for data cleaning → harmonization → validation → SQL generation
- Dual analytical framework:
  - Relational querying (MySQL)
  - Graph-based modeling (Neo4j)
- Quantitative validation ensuring data integrity and reproducibility

Outcome:
A high-fidelity, scalable database enabling robust clinical-genomic integration and downstream biological discovery.

---

## 2. System Architecture Overview

### Data Flow
Raw Data → Cleaning → Harmonization → Validation → SQL Generation → MySQL → Neo4j

### Design Principles
- Gene-centric integration
- Strict normalization (5NF)
- Deterministic transformations
- Elimination of redundancy
- Analytical scalability

---

## 3. Technology Stack

### Core Systems
- DBMS: MySQL
- Programming: Python
- Graph DB: Neo4j

### Python Ecosystem
- pandas
- numpy
- pathlib

### Data Standards
- HGNC gene mapping
- TCGA sample identifiers
- Simplified MAF mutation structure

---

## 4. Repository Architecture

project_root/

├── data_raw/              
Original datasets  

├── data_cleaned/          
Cleaned datasets  

├── scripts/               
Pipeline scripts  

├── sql/                  
schema.sql  
FINAL_POPULATE.sql  
queries.sql  

├── docs/                 
ERD  
Data Dictionary  
Writeup  

└── neo4j/                
neo4j_import.cypher  
For_Neo4j.csv  

---

## 5. Data Engineering Strategy

### Inclusion Criteria
- Direct biological interpretability
- Gene-level compatibility
- Cross-dataset linkage
- Analytical value

### Exclusion Criteria
- Arm-level CNA
- Segment-based CNA
- Methylation
- RPPA
- Structural variants
- Timeline and treatment data

This ensures a clean, gene-centered dataset.

---

## 6. Data Pipeline

### Stage 1: Cleaning
- Clinical normalization
- Mutation processing and VAF calculation
- CNA and expression reshaping

### Stage 2: Sample Harmonization
- Intersection across all datasets

### Stage 3: Gene Harmonization
- Common gene intersection

### Stage 4: Identifier Standardization
- HGNC mapping

### Stage 5: Final Integration
- Fully matched datasets

### Stage 6: Validation
- Patients: 499
- Samples: 499
- Genes: 12,311
- Mutations: 33,653

### Stage 7: SQL Generation
- Automated INSERT statements

Run pipeline:
python run_pipeline.py

---

## 7. Database Design

Entities:
- Patient
- Diagnosis
- Sample
- Gene
- Mutation
- Copy_Number_Alteration
- Expression

Features:
- 5NF normalization
- Many-to-many relationships handled correctly
- Strict constraints for integrity

---

## 8. SQL Analysis

Supports:
- Survival analysis
- Mutation burden
- Gene frequency
- CNA analysis
- High-VAF filtering

All queries are scalable and non-redundant.

---

## 9. Graph Database (Neo4j)

Nodes:
- Sample
- Gene

Relationships:
- HAS_GENE

Attributes:
- IDH status
- Codeletion status

Purpose:
- Network-based mutation analysis
- Subtype visualization

---

## 10. Biological Insights

- TP53 and ATRX enriched in IDH-mutant tumors
- CIC and FUBP1 enriched in codeleted tumors
- Strong subtype-specific mutation patterns

---

## 11. Validation

- Exact match between pipeline and database
- No duplication
- No orphan records
- Verified population

---

## 12. Reproducibility

Includes:
- Dataset selection table
- ERD
- 5NF schema
- Python pipeline
- SQL scripts
- Query outputs
- Neo4j analysis

---

## 13. How to Reproduce

1. Install:
   - Python
   - MySQL

2. Run:
python run_pipeline.py

3. Create DB:
mysql < schema.sql

4. Populate:
mysql < FINAL_POPULATE.sql

5. Validate:
mysql < queries.sql

---

## 14. Documentation

Located in /docs/:
- ERD
- Data dictionary
- Full write-up
- Validation report

