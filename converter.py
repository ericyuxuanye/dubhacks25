import pandas as pd
from pathlib import Path

# Folder where your UniProt TSV files are stored
base = Path(".")

# Collect all TSVs starting with "uniprotkb_Malus_domestica_"
tsv_files = list(base.glob("uniprotkb_Malus_domestica_*.tsv"))

rows = []
for f in tsv_files:
    df = pd.read_csv(f, sep="\t")
    for _, row in df.iterrows():
        entry = {
            "entry_id": row.get("Entry", ""),
            "species": row.get("Organism", "Malus × domestica (Golden Delicious)"),
            "protein_name": row.get("Protein names", ""),
            "gene_names": row.get("Gene Names", ""),
            "go_terms": "",  # UniProt TSV basic export doesn't include GO, keep blank
            "keywords": "",
            "pathways": "",
            "evidence_url": f"https://www.uniprot.org/uniprotkb/{row.get('Entry', '')}",
        }
        # Guess the trait bucket based on filename or protein name
        name_lower = f.name.lower()
        if "ft" in name_lower:
            entry["trait_bucket"] = "flowering"
        elif "tfl1" in name_lower:
            entry["trait_bucket"] = "flowering"
        elif "myb" in name_lower:
            entry["trait_bucket"] = "wood_strength"
        else:
            entry["trait_bucket"] = ""
        rows.append(entry)

# Convert to DataFrame
out_df = pd.DataFrame(rows, columns=[
    "entry_id", "species", "protein_name", "gene_names",
    "go_terms", "keywords", "pathways", "evidence_url", "trait_bucket"
])

out_path = base / "uniprot_genes.csv"
out_df.to_csv(out_path, index=False)
print(f"Wrote {len(out_df)} rows to {out_path}")
