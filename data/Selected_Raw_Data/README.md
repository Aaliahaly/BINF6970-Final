# Selected Raw Data
This folder contains the subset of files extracted from the original TCGA LGG dataset for use in this project.

## Description
The files in this folder were selected based on their relevance to gene-level, sample-level, and clinical analysis. No cleaning, transformation, or preprocessing has been applied. The data remains in its original format as downloaded from cBioPortal.
Relevant/Selected Data from data_clinical_patient.txt, data_clinical_sample.txt were combined into Clinical&Sample(1).xlsx.

## Purpose
These files serve as the direct input to the data cleaning stage. 
All subsequent steps, including cleaning, harmonization, validation, and database construction, are performed using these datasets.

## Files Included
- Clinical&Sample(1).xlsx
- data_mutations.txt (compressed)  
- data_cna.txt (compressed)  

## Note
The file `data_mrna_seq_v2_rsem.txt` is not included in this repository due to its large size. It should be downloaded directly from the original TCGA LGG dataset on cBioPortal to ensure full reproducibility.

