# SQL Database Files

This directory documents the SQL database files used to create, populate, and reconstruct the relational database for the TCGA Lower Grade Glioma multi-omics database project.

All SQL files are hosted externally on Figshare.

---

## Figshare Link

| Dataset | Link |
|---|---|
| SQL database files | https://doi.org/10.6084/m9.figshare.32204706 |

---

## Overview

The SQL files represent the relational database implementation stage of the project.

After the TCGA LGG datasets were cleaned, validated, sample-harmonized, gene-harmonized, HGNC-mapped, and finally harmonized, the resulting database-ready files were used to construct a structured SQL database.

The SQL database was designed to support integrated querying across patients, samples, genes, clinical features, mutations, copy number alteration records, and mRNA expression records.

---

## SQL Files Hosted on Figshare

The complete SQL dataset contains the following files:

| File | Description |
|---|---|
| `01_create_database_schema.sql` | Creates the database schema, including tables, fields, primary keys, foreign keys, and relationships. |
| `02_load_cleaned_data.sql.zip` | Compressed SQL file used to load the cleaned and harmonized data into the database. |
| `03_mydump.sql.zip` | Compressed SQL dump file used to reconstruct the populated database. |

---

## Purpose

The purpose of these SQL files is to make the relational database fully reproducible.

The schema file defines the database structure. It specifies how patients, samples, genes, clinical records, mutation records, CNA records, and expression records are stored and connected.

The loading file supports population of the database using the final harmonized datasets.

The dump file provides a complete database reconstruction option for users who want to recreate the populated database directly.

---

## Database Construction Workflow

The SQL database construction follows these steps:

1. Download the SQL files from the Figshare link above.
2. Unzip the compressed SQL files.
3. Create the database schema using `01_create_database_schema.sql`.
4. Load the harmonized data using `02_load_cleaned_data.sql`.
5. Alternatively, reconstruct the populated database directly using `03_mydump.sql`.

---

## How to Use

After downloading the files from Figshare, create the database schema using:

```bash
mysql -u root -p < 01_create_database_schema.sql
```

To load the cleaned and harmonized data, run:

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

To reconstruct the populated database from the dump file, run:

```bash
mysql -u root -p Database < 03_mydump.sql
```

Replace `Database` with the actual database name used in your local MySQL environment.

---

## Expected Result

After successful execution, the SQL database should contain the relational structure and populated tables required for the TCGA LGG multi-omics database.

The resulting database supports structured queries involving patients, samples, genes, clinical features, mutations, copy number alterations, and mRNA expression records.

---

## Notes

This GitHub directory serves as documentation for the SQL component of the project.

The SQL files themselves are hosted on Figshare to keep the GitHub repository lightweight and reproducible.

The SQL database is intended to support relational querying of the final harmonized TCGA LGG multi-omics data.
