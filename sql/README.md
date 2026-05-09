# SQL Database Files

This directory documents the SQL files used to build, populate, export, and reconstruct the MySQL relational database for the TCGA Lower Grade Glioma multi-omics database project.

---

## Figshare Link

| Dataset | Link |
|---|---|
| SQL Database Files | https://doi.org/10.6084/m9.figshare.32204706 |

---

## Overview

The SQL files represent the relational database implementation stage of the project.

After the TCGA LGG datasets were cleaned, validated, sample-harmonized, gene-harmonized, HGNC-mapped, and fully integrated, the final database-ready files were used to construct a structured MySQL database.

The SQL database was designed to support integrated querying across patients, diagnoses, samples, genes, clinical features, mutations, copy number alteration records, mRNA expression records, survival outcomes, and sample-level molecular features.

---

## SQL Files Hosted on Figshare

The complete SQL dataset contains the following files:

| File | Description |
|---|---|
| `01_create_database_schema.sql` | Creates the database schema, including tables, fields, primary keys, foreign keys, and relationships. |
| `02_load_cleaned_data.sql.zip` | Compressed SQL loading file used to populate the database after the schema has been created. |
| `03_mydump.sql.zip` | Compressed MySQL dump file used to reconstruct the complete populated database directly. |

After downloading the compressed SQL files from Figshare, unzip them before running the MySQL commands.

After unzipping, the files should be available as:

```text
01_create_database_schema.sql
02_load_cleaned_data.sql
03_mydump.sql
```

---

## Purpose

The purpose of these SQL files is to make the relational database fully reproducible.

Users can recreate the database in one of two ways.

The first option is to build and populate the database step by step. This option uses the schema file first, then uses the SQL loading file to insert the cleaned and harmonized data.

The second option is to reconstruct the already populated database directly from the MySQL dump file.

Both options produce the same final relational database.

---

## Database Reconstruction Options

After downloading the SQL files from Figshare and unzipping the compressed files, the database can be recreated using one of the following two options.

---

## Option 1: Build and Populate the Database

Use this option if you want to recreate the database construction process step by step.

This option uses:

- `01_create_database_schema.sql`
- `02_load_cleaned_data.sql`

First, create the database schema:

```bash
mysql -u root -p < 01_create_database_schema.sql
```

Then, populate the database using the cleaned and harmonized data-loading file:

```bash
mysql -u root -p Database < 02_load_cleaned_data.sql
```

This option creates the relational structure first and then loads the processed TCGA LGG multi-omics data into the database.

---

## Option 2: Reconstruct the Populated Database from the SQL Dump

Use this option if you want to recreate the complete populated database directly.

This option uses:

- `03_mydump.sql`

To restore the populated database from the dump file, run:

```bash
mysql -u root -p Database < 03_mydump.sql
```

This option restores the complete populated database without running the separate schema-creation and data-loading steps.

---

## Exporting the Database as a MySQL Dump

After building and populating the database, the populated MySQL database can be exported as a dump file using:

```bash
mysqldump --single-transaction -h 127.0.0.1 -P 3306 -u root -p Database > 03_mydump.sql
```

This command creates a dump file named:

```text
03_mydump.sql
```

The dump file can be used later to reconstruct the complete populated database directly.

---

## Notes on the Database Name

`Database` is the database name used in this project.

If you use a different database name in your local MySQL environment, replace `Database` with your own database name.

For example, to load the database using a different database name:

```bash
mysql -u root -p YourDatabaseName < 02_load_cleaned_data.sql
```

Or, to restore the dump using a different database name:

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
- Sample-level molecular features

---

## Reproducibility

This SQL directory supports reproducibility by providing two database reconstruction routes.

### Route 1: Build and Populate

This route uses:

- `01_create_database_schema.sql`
- `02_load_cleaned_data.sql`

This route is useful for users who want to inspect the database structure and understand how the cleaned and harmonized data are loaded into the relational database.

### Route 2: Direct Reconstruction from Dump

This route uses:

- `03_mydump.sql`

This route is useful for users who want to restore the complete populated database directly.

Both routes allow the same final SQL database to be recreated.

---

## Notes

The SQL files are hosted on Figshare because some files are too large to store directly in GitHub.

The compressed SQL files must be unzipped before use.

The SQL database is intended to support relational querying of the final harmonized TCGA LGG multi-omics data.

The Neo4j graph database files are documented separately and hosted in a separate Figshare dataset.
