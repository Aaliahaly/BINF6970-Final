"""
This script orchestrates the full multi-omics data processing pipeline.

What this script does:
- Executes all pipeline steps in sequence
- Ensures proper order of data harmonization and validation
- Produces final integrated datasets and validation report

Pipeline steps:
1. Data cleaning
2. Data validation
3. Sample-level harmonization
4. Gene-level harmonization
5. HGNC-based gene identifier mapping
6. Final dataset alignment
7. Validation and proof report generation
"""

# =========================
# IMPORT SCRIPTS
# =========================
import 01_clean_clinical_sample
import 02_clean_cna
import 03_clean_expression
import 04_clean_mutations
import 05_validator
import 06_sample_harmonization
import 07_gene_harmonization
import 08_hgnc_mapping
import 09_finalize
import 10_report


def run_all():
    # =========================
    # STEP 0: CLEANING
    # =========================
    print("STEP 0 - DATA CLEANING")
    01_clean_clinical_sample.run()
    02_clean_cna.run()
    03_clean_expression.run()
    04_clean_mutations.run()

    # =========================
    # STEP 1: VALIDATION
    # =========================
    print("\nSTEP 1 - DATA VALIDATION")
    05_validator.run()

    # =========================
    # STEP 2: SAMPLE HARMONIZATION
    # =========================
    print("\nSTEP 2 - SAMPLE HARMONIZATION")
    06_sample_harmonization.run()

    # =========================
    # STEP 3: GENE HARMONIZATION
    # =========================
    print("\nSTEP 3 - GENE HARMONIZATION")
    07_gene_harmonization.run()

    # =========================
    # STEP 4: HGNC MAPPING
    # =========================
    print("\nSTEP 4 - HGNC MAPPING")
    08_hgnc_mapping.run()

    # =========================
    # STEP 5: FINAL ALIGNMENT
    # =========================
    print("\nSTEP 5 - FINAL ALIGNMENT")
    09_finalize.run()

    # =========================
    # STEP 6: FINAL REPORT
    # =========================
    print("\nSTEP 6 - FINAL PROOF REPORT")
    10_report.run()


# =========================
# RUN FULL PIPELINE
# =========================
if __name__ == "__main__":
    run_all()
