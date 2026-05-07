# SQL Database Files

This directory documents the SQL database files used to create, populate, export, and reconstruct the relational database for the TCGA Lower Grade Glioma multi-omics database project.

All large SQL files are hosted externally on Figshare to keep the GitHub repository lightweight and reproducible.

---

## Figshare Link

| Dataset | Link |
|---|---|
| SQL Database Files | https://doi.org/10.6084/m9.figshare.32204706 |

---

## Overview

The SQL files represent the relational database implementation stage of the project.

After the TCGA LGG datasets were cleaned, validated, sample-harmonized, gene-harmonized, HGNC-mapped, and finally harmonized, the resulting database-ready files were used to construct a structured MySQL database.

The SQL database was designed to support integrated querying across patients, diagnoses, samples, genes, clinical features, mutations, copy number alteration records, and mRNA expression records.

---

## SQL Files Hosted on Figshare

The complete SQL dataset contains the following files:

| File | Description |
|---|---|
| `01_create_database_schema.sql` | Creates the database schema, including tables, fields, primary keys, foreign keys, and relationships. |
| `02_load_cleaned_data.sql.zip` | Compressed SQL file used to load the cleaned and harmonized data into the database. |
| `03_mydump.sql.zip` | Compressed SQL dump file used to reconstruct the populated database directly. |

---

## Purpose

The purpose of these SQL files is to make the relational database fully reproducible.

The schema file defines the database structure. It specifies how patients, diagnoses, samples, genes, clinical records, mutation records, CNA records, expression records, survival records, and sample features are stored and connected.

The loading file supports population of the database using the final harmonized datasets.

The dump file provides a complete database reconstruction option for users who want to recreate the populated database directly without rerunning the data-loading process.

---

## Database Construction Workflow

The SQL database construction follows these steps:

1. Download the SQL files from the Figshare link above.
2. Unzip the compressed SQL files.
3. Create the database schema using `01_create_database_schema.sql`.
4. Load the harmonized data using `02_load_cleaned_data.sql`.

Alternatively, users can reconstruct the populated database directly using `03_mydump.sql`.

---

## How to Use

After downloading the SQL files from Figshare, you can rebuild the database in two ways.

You can either create the schema and load the cleaned and harmonized data manually, or you can download and use the SQL dump file to reconstruct the populated database directly.

---

### Option 1: Create the schema and load the cleaned data

To create the database schema, run:

```bash
mysql -u root -p < 01_create_database_schema.sql
```

To load the cleaned and harmonized data into the database, run:

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

---

### Option 2: Reconstruct the populated database from the SQL dump

You can also download the SQL dump file from Figshare and use it to reconstruct the populated database directly.

To restore the populated database from the dump file, run:

```bash
mysql -u root -p Database < 03_mydump.sql
```

---

## Exporting the Database as a MySQL Dump

After building and populating the database, you can export the populated database as a MySQL dump file.

Run:

```bash
mysqldump --single-transaction -h 127.0.0.1 -P 3306 -u root -p Database > 03_mydump.sql
```

This command creates a dump file named:

```text
03_mydump.sql
```

This file can be used later to reconstruct the populated database directly.

---

## Notes on the Database Name

`Database` is the database name used in this project.

If you use a different database name in your local MySQL environment, replace `Database` with your own database name.

For example:

```bash
mysql -u root -p YourDatabaseName < 02_load_cleaned_data.sql
```

or:

```bash
mysql -u root -p YourDatabaseName < 03_mydump.sql
```

---

## Expected Result

After successful execution, the MySQL database should contain the full relational structure and populated tables required for the TCGA LGG multi-omics database.

The resulting database supports structured queries involving:

- Patients
- Diagnoses
- Samples
- Genes
- Clinical features
- Mutations
- Sample-mutation relationships
- Copy number alterations
- mRNA expression records
- Survival outcomes
- Sample-level features

---

## Reproducibility

This SQL directory supports reproducibility by providing three database reconstruction options:

1. Rebuild the database schema from `01_create_database_schema.sql`.
2. Populate the database using `02_load_cleaned_data.sql`.
3. Restore the populated database directly using `03_mydump.sql`.

This ensures that users can recreate the database either from the structured loading file or from the complete SQL dump.

---

## Notes

The SQL files themselves are hosted on Figshare because some files are too large to store directly in GitHub.

The SQL database is intended to support relational querying of the final harmonized TCGA LGG multi-omics data.

The Neo4j graph database files are documented separately and hosted in a separate Figshare dataset.
