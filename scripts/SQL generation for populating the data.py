from pathlib import Path
import pandas as pd
import math

# ============================================================
# SETTINGS
# ============================================================

DATA_DIR = Path.home() / "Desktop" / "Step4"
OUTPUT_SQL = DATA_DIR / "FINAL_POPULATE.sql"

CLINICAL_FILE = DATA_DIR / "clin_FINAL.xlsx"
MUTATION_FILE = DATA_DIR / "mut_FINAL.xlsx"
CNA_FILE = DATA_DIR / "cna_FINAL.csv"
EXPRESSION_FILE = DATA_DIR / "expr_FINAL.csv"

# Keep this small enough so MySQL does not crash
CHUNK_SIZE = 500

# ============================================================
# HELPERS
# ============================================================

def is_missing(x):
    if x is None:
        return True
    try:
        if pd.isna(x):
            return True
    except Exception:
        pass
    s = str(x).strip()
    return s == "" or s.lower() == "nan"


def clean(x):
    if is_missing(x):
        return None
    return str(x).strip()


def clean_int(x):
    if is_missing(x):
        return None
    try:
        return int(float(x))
    except Exception:
        return None


def clean_float(x):
    if is_missing(x):
        return None
    try:
        return round(float(x), 2)
    except Exception:
        return None


def sql(x):
    if x is None:
        return "NULL"
    if isinstance(x, bool):
        return "1" if x else "0"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        if math.isnan(x):
            return "NULL"
        return str(round(x, 2))
    s = str(x).replace("\\", "\\\\").replace("'", "''")
    return f"'{s}'"


def write_insert(f, table, cols, rows):
    if not rows:
        return

    for i in range(0, len(rows), CHUNK_SIZE):
        chunk = rows[i:i + CHUNK_SIZE]

        f.write(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n")

        values = []
        for r in chunk:
            values.append("(" + ", ".join(sql(v) for v in r) + ")")

        f.write(",\n".join(values))
        f.write(";\n\n")


def normalize_columns(df):
    df.columns = [str(c).strip() for c in df.columns]
    return df


def build_attr_map(df):
    """
    Build a case-insensitive and punctuation-friendly lookup.
    Example:
    Overall Survival Status -> overallsurvivalstatus
    """
    attr_map = {}
    for col in df.columns:
        key = "".join(ch.lower() for ch in str(col) if ch.isalnum())
        attr_map[key] = col
    return attr_map


def get_col(df, *names, required=True):
    """
    Find a column by trying several alternative names.
    """
    attr_map = build_attr_map(df)

    for name in names:
        key = "".join(ch.lower() for ch in str(name) if ch.isalnum())
        if key in attr_map:
            return attr_map[key]

    if required:
        raise ValueError(f"Missing required column. Tried: {names}")
    return None


def normalize_cna_value(status_value, numeric_value):
    """
    If CNA_Value exists and is numeric, use it.
    Otherwise infer it from CNA_Status.
    Common mapping:
      deep loss / deletion / homozygous deletion -> -2
      loss / shallow deletion / hemizygous deletion -> -1
      neutral / diploid -> 0
      gain -> 1
      amplification / amp -> 2
    """
    num = clean_int(numeric_value)
    if num is not None:
        return num

    status = clean(status_value)
    if status is None:
        return None

    s = status.lower().strip()

    mapping = {
        "deep loss": -2,
        "deep deletion": -2,
        "homozygous deletion": -2,
        "homdel": -2,
        "deletion": -2,

        "loss": -1,
        "shallow loss": -1,
        "shallow deletion": -1,
        "hemizygous deletion": -1,
        "single copy deletion": -1,

        "neutral": 0,
        "diploid": 0,
        "normal": 0,
        "no change": 0,

        "gain": 1,
        "copy gain": 1,
        "low gain": 1,

        "amplification": 2,
        "amp": 2,
        "high amplification": 2,
        "high amp": 2,
    }

    return mapping.get(s, None)


# ============================================================
# LOAD FILES
# ============================================================

print("Reading files...")

clinical = pd.read_excel(CLINICAL_FILE)
mutation = pd.read_excel(MUTATION_FILE)
cna = pd.read_csv(CNA_FILE)
expression = pd.read_csv(EXPRESSION_FILE)

clinical = normalize_columns(clinical)
mutation = normalize_columns(mutation)
cna = normalize_columns(cna)
expression = normalize_columns(expression)

print("Files loaded successfully.")

# ============================================================
# CLINICAL COLUMN MAPPING
# ============================================================

patient_id_col = get_col(clinical, "Patient_ID")
sample_id_col = get_col(clinical, "Sample_ID")

gender_col = get_col(clinical, "Gender", required=False)
ancestry_col = get_col(clinical, "Genetic_Ancestry_Label", required=False)

diagnosis_age_col = get_col(clinical, "Diagnosis_Age", required=False)

cancer_site_col = get_col(clinical, "Cancer_Site", required=False)
cancer_type_col = get_col(clinical, "Cancer_Type", required=False)
cancer_hist_col = get_col(clinical, "Cancer_Histological_Type", required=False)

sample_type_col = get_col(clinical, "Sample_Type", required=False)
grade_col = get_col(clinical, "Tumor_Histologic_Grade", required=False)
aneuploidy_col = get_col(clinical, "Aneuploidy_Score", required=False)
somatic_col = get_col(clinical, "Somatic_Status", required=False)
idh_col = get_col(clinical, "IDH_Status", required=False)
codeletion_col = get_col(clinical, "Codeletion_Status", required=False)

# Survival columns
os_status_col = get_col(clinical, "Overall_Survival_Status", required=False)
os_months_col = get_col(clinical, "Overall_Survival_Months", required=False)

dss_status_col = get_col(clinical, "Disease_Specific_Survival_Status", required=False)
dss_months_col = get_col(clinical, "Disease_Specific_Survival_Months", required=False)

dfs_status_col = get_col(clinical, "Disease_Free_Status", required=False)
dfs_months_col = get_col(clinical, "Disease_Free_Months", required=False)

pfs_status_col = get_col(clinical, "Progression_Free_Status", required=False)
pfs_months_col = get_col(clinical, "Progression_Free_Months", required=False)

# Hypoxia feature columns
buffa_col = get_col(clinical, "Buffa_Hypoxia_Score", required=False)
winter_col = get_col(clinical, "Winter_Hypoxia_Score", required=False)
ragnum_col = get_col(clinical, "Ragnum_Hypoxia_Score", required=False)

# ============================================================
# MUTATION COLUMN MAPPING
# ============================================================

mut_gene_col = get_col(mutation, "Hugo_Symbol", required=False)
mut_entrez_col = get_col(mutation, "Entrez_Gene_Id", "Entrez_Gene_ID", required=False)
mut_chr_col = get_col(mutation, "Chromosome", required=False)
mut_start_col = get_col(mutation, "Start_Position", required=False)
mut_end_col = get_col(mutation, "End_Position", required=False)
mut_ref_col = get_col(mutation, "Reference_Allele", required=False)
mut_alt_col = get_col(mutation, "Tumor_Seq_Allele", "Tumor_Seq_Allele2", required=False)
mut_type_col = get_col(mutation, "Variant_Type", required=False)
mut_class_col = get_col(mutation, "Variant_Classification", required=False)
mut_consequence_col = get_col(mutation, "Primary_Consequence", required=False)
mut_impact_col = get_col(mutation, "Impact_Level", required=False)
mut_vaf_col = get_col(mutation, "VAF", required=False)
mut_sample_col = get_col(mutation, "Sample_ID", "Tumor_Sample_Barcode", required=False)

# ============================================================
# CNA COLUMN MAPPING
# ============================================================

cna_gene_col = get_col(cna, "Hugo_Symbol", required=False)
cna_entrez_col = get_col(cna, "Entrez_Gene_Id", "Entrez_Gene_ID", required=False)
cna_sample_col = get_col(cna, "Sample_ID", required=False)
cna_status_col = get_col(cna, "CNA_Status", required=False)
cna_value_col = get_col(cna, "CNA_Value", required=False)

# ============================================================
# EXPRESSION COLUMN MAPPING
# ============================================================

expr_gene_col = get_col(expression, "Hugo_Symbol", required=False)
expr_entrez_col = get_col(expression, "Entrez_Gene_Id", "Entrez_Gene_ID", required=False)
expr_sample_col = get_col(expression, "Sample_ID", required=False)
expr_value_col = get_col(expression, "Expression", "Expression_Value", required=False)
expr_type_col = get_col(expression, "Expression_Type", required=False)

# ============================================================
# PATIENT
# ============================================================

print("Building Patient table rows...")

patient_df = clinical[[patient_id_col]].copy()
patient_df["Gender"] = clinical[gender_col] if gender_col else None
patient_df["Genetic_Ancestry_Label"] = clinical[ancestry_col] if ancestry_col else None
patient_df = patient_df.drop_duplicates(subset=[patient_id_col])

patient_rows = []
for _, r in patient_df.iterrows():
    patient_rows.append((
        clean(r[patient_id_col]),
        clean(r["Gender"]),
        clean(r["Genetic_Ancestry_Label"])
    ))

# ============================================================
# CANCER
# ============================================================

print("Building Cancer table rows...")

cancer_df = pd.DataFrame({
    "Cancer_Site": clinical[cancer_site_col] if cancer_site_col else None,
    "Cancer_Type": clinical[cancer_type_col] if cancer_type_col else None,
    "Cancer_Histological_Type": clinical[cancer_hist_col] if cancer_hist_col else None,
}).drop_duplicates()

cancer_rows = []
cancer_map = {}
cid = 1

for _, r in cancer_df.iterrows():
    key = (
        clean(r["Cancer_Site"]),
        clean(r["Cancer_Type"]),
        clean(r["Cancer_Histological_Type"])
    )
    if key not in cancer_map:
        cancer_map[key] = cid
        cancer_rows.append(key)
        cid += 1

# ============================================================
# DIAGNOSIS
# ============================================================

print("Building Diagnosis table rows...")

diagnosis_rows = []
diag_map = {}
did = 1

diagnosis_df = clinical.drop_duplicates(subset=[patient_id_col]).copy()

for _, r in diagnosis_df.iterrows():
    patient_id = clean(r[patient_id_col])

    cancer_key = (
        clean(r[cancer_site_col]) if cancer_site_col else None,
        clean(r[cancer_type_col]) if cancer_type_col else None,
        clean(r[cancer_hist_col]) if cancer_hist_col else None
    )

    diagnosis_rows.append((
        patient_id,
        cancer_map.get(cancer_key),
        clean_int(r[diagnosis_age_col]) if diagnosis_age_col else None
    ))

    diag_map[patient_id] = did
    did += 1

# ============================================================
# SURVIVAL
# ============================================================

print("Building Survival table rows...")

survival_rows = []

survival_df = clinical.drop_duplicates(subset=[patient_id_col]).copy()

for _, r in survival_df.iterrows():
    patient_id = clean(r[patient_id_col])
    diagnosis_id = diag_map.get(patient_id)

    survival_rows.append((
        diagnosis_id,
        clean(r[os_status_col]) if os_status_col else None,
        clean_float(r[os_months_col]) if os_months_col else None,
        clean(r[dfs_status_col]) if dfs_status_col else None,
        clean_float(r[dfs_months_col]) if dfs_months_col else None,
        clean(r[pfs_status_col]) if pfs_status_col else None,
        clean_float(r[pfs_months_col]) if pfs_months_col else None,
        clean(r[dss_status_col]) if dss_status_col else None,
        clean_float(r[dss_months_col]) if dss_months_col else None
    ))

# ============================================================
# SAMPLE
# ============================================================

print("Building Sample table rows...")

sample_rows = []
valid_sample_ids = set()

sample_df = clinical.drop_duplicates(subset=[sample_id_col]).copy()

for _, r in sample_df.iterrows():
    sample_id = clean(r[sample_id_col])
    patient_id = clean(r[patient_id_col])

    if sample_id is None:
        continue

    valid_sample_ids.add(sample_id)

    sample_rows.append((
        sample_id,
        diag_map.get(patient_id),
        clean(r[sample_type_col]) if sample_type_col else None,
        clean(r[grade_col]) if grade_col else None,
        clean_int(r[aneuploidy_col]) if aneuploidy_col else None,
        clean(r[somatic_col]) if somatic_col else None,
        clean(r[idh_col]) if idh_col else None,
        clean(r[codeletion_col]) if codeletion_col else None
    ))

# ============================================================
# GENE
# ============================================================

print("Building Gene table rows...")

gene_set = set()

for _, r in mutation.iterrows():
    gene_set.add((
        clean_int(r[mut_entrez_col]) if mut_entrez_col else None,
        clean(r[mut_gene_col]) if mut_gene_col else None
    ))

for _, r in cna.iterrows():
    gene_set.add((
        clean_int(r[cna_entrez_col]) if cna_entrez_col else None,
        clean(r[cna_gene_col]) if cna_gene_col else None
    ))

for _, r in expression.iterrows():
    gene_set.add((
        clean_int(r[expr_entrez_col]) if expr_entrez_col else None,
        clean(r[expr_gene_col]) if expr_gene_col else None
    ))

# Remove fully empty genes
gene_set = {g for g in gene_set if g[0] is not None or g[1] is not None}

gene_rows = []
gene_map = {}
gid = 1

for g in sorted(gene_set, key=lambda x: (x[0] is None, x[0], x[1] is None, str(x[1]))):
    gene_map[g] = gid
    gene_rows.append(g)
    gid += 1

# ============================================================
# MUTATION
# ============================================================

print("Building Mutation table rows...")

mutation_rows = []
mut_map = {}
mid = 1

for _, r in mutation.iterrows():
    gene_key = (
        clean_int(r[mut_entrez_col]) if mut_entrez_col else None,
        clean(r[mut_gene_col]) if mut_gene_col else None
    )
    gene_id = gene_map.get(gene_key)

    mkey = (
        gene_id,
        clean(r[mut_chr_col]) if mut_chr_col else None,
        clean_int(r[mut_start_col]) if mut_start_col else None,
        clean_int(r[mut_end_col]) if mut_end_col else None,
        clean(r[mut_ref_col]) if mut_ref_col else None,
        clean(r[mut_alt_col]) if mut_alt_col else None,
        clean(r[mut_type_col]) if mut_type_col else None,
        clean(r[mut_class_col]) if mut_class_col else None,
        clean(r[mut_consequence_col]) if mut_consequence_col else None,
        clean(r[mut_impact_col]) if mut_impact_col else None
    )

    if mkey not in mut_map:
        mut_map[mkey] = mid
        mutation_rows.append(mkey)
        mid += 1

# ============================================================
# SAMPLE_MUTATION
# ============================================================

print("Building Sample_Mutation table rows...")

sample_mut_rows = []
sample_mut_seen = set()

if mut_sample_col:
    for _, r in mutation.iterrows():
        gene_key = (
            clean_int(r[mut_entrez_col]) if mut_entrez_col else None,
            clean(r[mut_gene_col]) if mut_gene_col else None
        )
        gene_id = gene_map.get(gene_key)

        mkey = (
            gene_id,
            clean(r[mut_chr_col]) if mut_chr_col else None,
            clean_int(r[mut_start_col]) if mut_start_col else None,
            clean_int(r[mut_end_col]) if mut_end_col else None,
            clean(r[mut_ref_col]) if mut_ref_col else None,
            clean(r[mut_alt_col]) if mut_alt_col else None,
            clean(r[mut_type_col]) if mut_type_col else None,
            clean(r[mut_class_col]) if mut_class_col else None,
            clean(r[mut_consequence_col]) if mut_consequence_col else None,
            clean(r[mut_impact_col]) if mut_impact_col else None
        )

        mutation_id = mut_map.get(mkey)
        sample_id = clean(r[mut_sample_col])

        if sample_id not in valid_sample_ids:
            continue
        if mutation_id is None:
            continue

        key = (mutation_id, sample_id)
        if key not in sample_mut_seen:
            sample_mut_seen.add(key)
            sample_mut_rows.append((
                mutation_id,
                sample_id,
                clean_float(r[mut_vaf_col]) if mut_vaf_col else None
            ))

# ============================================================
# COPY NUMBER ALTERATION
# ============================================================

print("Building Copy_Number_Alteration table rows...")

cna_rows = []

for _, r in cna.iterrows():
    sample_id = clean(r[cna_sample_col]) if cna_sample_col else None
    if sample_id not in valid_sample_ids:
        continue

    gene_key = (
        clean_int(r[cna_entrez_col]) if cna_entrez_col else None,
        clean(r[cna_gene_col]) if cna_gene_col else None
    )
    gene_id = gene_map.get(gene_key)

    if gene_id is None:
        continue

    cna_rows.append((
        sample_id,
        gene_id,
        normalize_cna_value(
            r[cna_status_col] if cna_status_col else None,
            r[cna_value_col] if cna_value_col else None
        ),
        clean(r[cna_status_col]) if cna_status_col else None
    ))

# ============================================================
# EXPRESSION
# ============================================================

print("Building Expression table rows...")

expr_rows = []
expr_seen = set()

for _, r in expression.iterrows():
    sample_id = clean(r[expr_sample_col]) if expr_sample_col else None
    if sample_id not in valid_sample_ids:
        continue

    gene_key = (
        clean_int(r[expr_entrez_col]) if expr_entrez_col else None,
        clean(r[expr_gene_col]) if expr_gene_col else None
    )
    gene_id = gene_map.get(gene_key)

    if gene_id is None:
        continue

    key = (sample_id, gene_id)
    if key in expr_seen:
        continue

    expr_seen.add(key)

    expr_rows.append((
        sample_id,
        gene_id,
        clean(r[expr_type_col]) if expr_type_col else None,
        clean_float(r[expr_value_col]) if expr_value_col else None
    ))

# ============================================================
# SAMPLE FEATURES DEFINITION
# ============================================================

print("Building Sample_Features_Definition table rows...")

feature_rows = []
feature_map = {}
next_feature_id = 1

if buffa_col:
    feature_rows.append(("Buffa_Hypoxia_Score",))
    feature_map["Buffa_Hypoxia_Score"] = next_feature_id
    next_feature_id += 1

if winter_col:
    feature_rows.append(("Winter_Hypoxia_Score",))
    feature_map["Winter_Hypoxia_Score"] = next_feature_id
    next_feature_id += 1

if ragnum_col:
    feature_rows.append(("Ragnum_Hypoxia_Score",))
    feature_map["Ragnum_Hypoxia_Score"] = next_feature_id
    next_feature_id += 1

# ============================================================
# SAMPLE_FEATURE
# ============================================================

print("Building Sample_Feature table rows...")

sample_feature_rows = []
sample_feature_seen = set()

sample_feature_df = clinical.drop_duplicates(subset=[sample_id_col]).copy()

for _, r in sample_feature_df.iterrows():
    sample_id = clean(r[sample_id_col])

    if sample_id not in valid_sample_ids:
        continue

    if buffa_col and "Buffa_Hypoxia_Score" in feature_map:
        key = (feature_map["Buffa_Hypoxia_Score"], sample_id)
        if key not in sample_feature_seen:
            sample_feature_seen.add(key)
            sample_feature_rows.append((
                feature_map["Buffa_Hypoxia_Score"],
                sample_id,
                clean_int(r[buffa_col])
            ))

    if winter_col and "Winter_Hypoxia_Score" in feature_map:
        key = (feature_map["Winter_Hypoxia_Score"], sample_id)
        if key not in sample_feature_seen:
            sample_feature_seen.add(key)
            sample_feature_rows.append((
                feature_map["Winter_Hypoxia_Score"],
                sample_id,
                clean_int(r[winter_col])
            ))

    if ragnum_col and "Ragnum_Hypoxia_Score" in feature_map:
        key = (feature_map["Ragnum_Hypoxia_Score"], sample_id)
        if key not in sample_feature_seen:
            sample_feature_seen.add(key)
            sample_feature_rows.append((
                feature_map["Ragnum_Hypoxia_Score"],
                sample_id,
                clean_int(r[ragnum_col])
            ))

# ============================================================
# WRITE SQL FILE
# ============================================================

print("Writing SQL file...")

with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
    f.write("SET FOREIGN_KEY_CHECKS=0;\n")
    f.write("SET UNIQUE_CHECKS=0;\n")
    f.write("SET AUTOCOMMIT=0;\n\n")

    f.write("-- Optional cleanup\n")
    f.write("DELETE FROM Sample_Feature;\n")
    f.write("DELETE FROM Sample_Features_Definition;\n")
    f.write("DELETE FROM Expression;\n")
    f.write("DELETE FROM Copy_Number_Alteration;\n")
    f.write("DELETE FROM Sample_Mutation;\n")
    f.write("DELETE FROM Mutation;\n")
    f.write("DELETE FROM Gene;\n")
    f.write("DELETE FROM Sample;\n")
    f.write("DELETE FROM Survival;\n")
    f.write("DELETE FROM Diagnosis;\n")
    f.write("DELETE FROM Cancer;\n")
    f.write("DELETE FROM Patient;\n\n")

    f.write("ALTER TABLE Cancer AUTO_INCREMENT = 1;\n")
    f.write("ALTER TABLE Diagnosis AUTO_INCREMENT = 1;\n")
    f.write("ALTER TABLE Survival AUTO_INCREMENT = 1;\n")
    f.write("ALTER TABLE Gene AUTO_INCREMENT = 1;\n")
    f.write("ALTER TABLE Mutation AUTO_INCREMENT = 1;\n")
    f.write("ALTER TABLE Copy_Number_Alteration AUTO_INCREMENT = 1;\n")
    f.write("ALTER TABLE Sample_Features_Definition AUTO_INCREMENT = 1;\n\n")

    write_insert(
        f,
        "Patient",
        ["Patient_ID", "Gender", "Genetic_Ancestry_Label"],
        patient_rows
    )

    write_insert(
        f,
        "Cancer",
        ["Cancer_Site", "Cancer_Type", "Cancer_Histological_Type"],
        cancer_rows
    )

    write_insert(
        f,
        "Diagnosis",
        ["Patient_ID", "Cancer_ID", "Diagnosis_Age"],
        diagnosis_rows
    )

    write_insert(
        f,
        "Survival",
        [
            "Diagnosis_ID",
            "Overall_Survival_Status",
            "Overall_Survival_Months",
            "Disease_Free_Status",
            "Disease_Free_Months",
            "Progression_Free_Status",
            "Progression_Free_Months",
            "Disease_Specific_Survival_Status",
            "Disease_Specific_Survival_Months"
        ],
        survival_rows
    )

    write_insert(
        f,
        "Sample",
        [
            "Sample_ID",
            "Diagnosis_ID",
            "Sample_Type",
            "Tumor_Histologic_Grade",
            "Aneuploidy_Score",
            "Somatic_Status",
            "IDH_Status",
            "Codeletion_Status"
        ],
        sample_rows
    )

    write_insert(
        f,
        "Gene",
        ["Entrez_Gene_ID", "Hugo_Symbol"],
        gene_rows
    )

    write_insert(
        f,
        "Mutation",
        [
            "Gene_ID",
            "Chromosome",
            "Start_Position",
            "End_Position",
            "Reference_Allele",
            "Tumor_Seq_Allele",
            "Variant_Type",
            "Variant_Classification",
            "Primary_Consequence",
            "Impact_Level"
        ],
        mutation_rows
    )

    write_insert(
        f,
        "Sample_Mutation",
        ["Mutation_ID", "Sample_ID", "VAF"],
        sample_mut_rows
    )

    write_insert(
        f,
        "Copy_Number_Alteration",
        ["Sample_ID", "Gene_ID", "CNA_Value", "CNA_Status"],
        cna_rows
    )

    write_insert(
        f,
        "Expression",
        ["Sample_ID", "Gene_ID", "Expression_Type", "Expression_Value"],
        expr_rows
    )

    write_insert(
        f,
        "Sample_Features_Definition",
        ["Feature_Name"],
        feature_rows
    )

    write_insert(
        f,
        "Sample_Feature",
        ["Feature_ID", "Sample_ID", "Value"],
        sample_feature_rows
    )

    f.write("COMMIT;\n\n")
    f.write("SET FOREIGN_KEY_CHECKS=1;\n")
    f.write("SET UNIQUE_CHECKS=1;\n")
    f.write("SET AUTOCOMMIT=1;\n")

print("Done.")
print(f"SQL file created: {OUTPUT_SQL}")
print()
print(f"Patients: {len(patient_rows)}")
print(f"Cancers: {len(cancer_rows)}")
print(f"Diagnoses: {len(diagnosis_rows)}")
print(f"Survival rows: {len(survival_rows)}")
print(f"Samples: {len(sample_rows)}")
print(f"Genes: {len(gene_rows)}")
print(f"Mutations: {len(mutation_rows)}")
print(f"Sample_Mutation rows: {len(sample_mut_rows)}")
print(f"CNA rows: {len(cna_rows)}")
print(f"Expression rows: {len(expr_rows)}")
print(f"Sample_Features_Definitions: {len(feature_rows)}")
print(f"Sample_Feature rows: {len(sample_feature_rows)}")
