import pandas as pd
from pathlib import Path

# =========================
# 1. LOAD FILE
# =========================
file_path = Path.home() / "Desktop" / "For Neo4j.csv"
df = pd.read_csv(file_path)

# =========================
# 2. CLEAN DATA
# =========================
df["Sample_ID"] = df["Sample_ID"].astype(str).str.strip()
df["Hugo_Symbol"] = df["Hugo_Symbol"].astype(str).str.strip()

# normalize case
df["IDH_Status"] = df["IDH_Status"].str.strip().str.capitalize()

# IMPORTANT: keep NaN as NaN (no astype(str))
df["Codeletion_Status"] = df["Codeletion_Status"].str.strip()

# =========================
# 3. FIX BIOLOGY RULE
# =========================
df.loc[df["IDH_Status"] == "Wildtype", "Codeletion_Status"] = None

# =========================
# 4. REMOVE EMPTY ROWS
# =========================
df = df[(df["Sample_ID"] != "") & (df["Hugo_Symbol"] != "")]

# =========================
# 5. GENERATE CYPHER
# =========================
cypher_lines = []

for _, row in df.iterrows():
    sample = row["Sample_ID"]
    gene = row["Hugo_Symbol"]
    idh = row["IDH_Status"]
    code = row["Codeletion_Status"]

    # handle NULL correctly
    if pd.isna(code):
        code_value = "NULL"
    else:
        code_value = f'"{code}"'

    cypher = f'''
MERGE (s:Sample {{Sample_ID: "{sample}"}})
SET s.idh_status = "{idh}",
    s.codeletion_status = {code_value}

MERGE (g:Gene {{Hugo_Symbol: "{gene}"}})
MERGE (s)-[:HAS_GENE]->(g);
'''
    cypher_lines.append(cypher)

# =========================
# 6. SAVE FILE
# =========================
output_file = Path.home() / "Desktop" / "neo4j_import.cypher"

with open(output_file, "w") as f:
    f.writelines(cypher_lines)

print("Clean Cypher file created!")