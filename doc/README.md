# Documentation

This `doc/` directory contains the main written documentation for the TCGA Lower Grade Glioma multi-omics database project.

The documentation provides the formal project report that explains the scientific rationale, data source selection, database design, processing workflow, SQL implementation, Neo4j graph analysis, biological interpretation, reproducibility steps, limitations, and future work.

---

## Main Documentation File

| File | Description |
|---|---|
| `Final Project Writeup.pdf` | Complete final project report for the TCGA LGG multi-omics database project. |

---

## What the Final Project Writeup Covers

The final project writeup includes:

- Project overview and rationale
- TCGA LGG data source selection
- Inclusion and exclusion decisions for source files
- Multi-omics database design strategy
- Entity-relationship diagram
- Relational schema design
- Normalization up to Fifth Normal Form
- Data dictionary
- Python pipeline structure
- Data cleaning and transformation decisions
- Dataset validation strategy
- Sample-level harmonization
- Gene-level harmonization
- HGNC-based gene identifier mapping
- Final harmonized database-ready datasets
- SQL database construction
- SQL database population
- SQL queries with rationale and outputs
- Neo4j graph database construction
- Graph-based analysis
- Key mutated gene annotation
- Biological interpretation
- Reproduction steps
- Project limitations
- Future work

---

## Relationship to Other Repository Directories

The PDF in this directory provides the formal written explanation of the project.

The other repository directories provide the files and instructions needed to reproduce or inspect each technical component.

| Directory | Purpose |
|---|---|
| `data/` | Provides Figshare links for selected inputs, intermediate outputs, final harmonized datasets, SQL files, and Neo4j files. |
| `scripts/` | Contains Python scripts for data cleaning, validation, harmonization, HGNC mapping, SQL population script generation, and Neo4j Cypher generation. |
| `sql/` | Documents the SQL schema file, SQL loading file, and SQL dump file used to build, populate, or reconstruct the MySQL database. |
| `diagrams/` | Contains database design diagrams, including the conceptual model and logical ERD. |

---

## Data and File Availability

Large datasets, SQL files, intermediate outputs, and graph database files are not stored in this directory.

They are hosted externally on Figshare because several files exceed practical GitHub storage limits.

The access links are provided in:

```text
data/README.md
```

and in the main project:

```text
README.md
```

---

## Intended Use

Use this directory when you want to read the complete formal project report.

Use the main repository README and the directory-specific README files when you want to reproduce the pipeline, rebuild the SQL database, inspect the data files, or generate the Neo4j graph database files.
