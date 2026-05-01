# Original TCGA LGG Dataset

This folder represents the complete set of files obtained when downloading the **Brain Lower Grade Glioma (TCGA, PanCancer Atlas)** dataset from cBioPortal.

## Source
https://www.cbioportal.org/study/summary?id=lgg_tcga_pan_can_atlas_2018

## Description
The dataset includes all original files provided by cBioPortal, covering multiple data types such as clinical data, mutation data, copy number alterations (CNA), gene expression, and associated metadata.
These files are kept in their original format and structure to preserve data integrity and ensure full reproducibility of the data processing pipeline.

## Note
All downstream cleaning, transformation, and integration steps in this project are performed using these original files as the starting point.
The following files have been compressed (zipped) to enable upload to this repository:
- `data_mutations.txt`
- `data_cna.txt`
- `data_log2_cna.txt`
- `data_mrna_seq_v2_rsem_zscores_ref_all_samples.txt`
- `data_mrna_seq_v2_rsem_zscores_ref_diploid_samples.txt`
The files `data_methylation_hm27_hm450_merged.txt` and `data_mrna_seq_v2_rsem.txt` are not included in this repository due to their large size. These files should be downloaded directly from the original data source if full reproduction is required.
