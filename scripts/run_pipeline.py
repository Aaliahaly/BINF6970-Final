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
import clean_clinical_sample
import clean_cna
import clean_expression
import clean_mutations
import validator
import sample_harmonization
import gene_harmonization
import hgnc_mapping
import finalize
import report


def run_all():
    # =========================
    # STEP 0: CLEANING
    # =========================
    print("STEP 0 - DATA CLEANING")
    clean_clinical_sample.run()
    clean_cna.run()
    clean_expression.run()
    clean_mutations.run()

    # =========================
    # STEP 1: VALIDATION
    # =========================
    print("\nSTEP 1 - DATA VALIDATION")
    validator.run()

    # =========================
    # STEP 2: SAMPLE HARMONIZATION
    # =========================
    print("\nSTEP 2 - SAMPLE HARMONIZATION")
    sample_harmonization.run()

    # =========================
    # STEP 3: GENE HARMONIZATION
    # =========================
    print("\nSTEP 3 - GENE HARMONIZATION")
    gene_harmonization.run()

    # =========================
    # STEP 4: HGNC MAPPING
    # =========================
    print("\nSTEP 4 - HGNC MAPPING")
    hgnc_mapping.run()

    # =========================
    # STEP 5: FINAL ALIGNMENT
    # =========================
    print("\nSTEP 5 - FINAL ALIGNMENT")
    finalize.run()

    # =========================
    # STEP 6: FINAL REPORT
    # =========================
    print("\nSTEP 6 - FINAL PROOF REPORT")
    report.run()


# =========================
# RUN FULL PIPELINE
# =========================
if __name__ == "__main__":
    run_all()
