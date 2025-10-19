import csv
import re
from pathlib import Path

# Configuration
TARGET_PATTERNS = re.compile(r'(FT|TFL1|CEN|AP1)', re.IGNORECASE)  # Match anywhere in symbol
CRISPR_PAM = re.compile(r'(?=(.{20}GG))')  # Find 20bp protospacers with NGG PAM
OUTPUT_DIR = Path('isolated_genes')
COMBINED_FASTA = Path('combined_sequences.fasta')

def process_fasta(fasta_str):
    """Clean and validate FASTA format"""
    try:
        # Handle both actual newlines and escaped \n sequences
        cleaned_fasta = fasta_str.strip('"').replace('\\n', '\n')
        lines = [line.strip() for line in cleaned_fasta.splitlines()]
        header = lines[0]
        
        if not header.startswith('>'):
            raise ValueError("Missing FASTA header")
            
        sequence = ''.join(lines[1:]).replace(' ', '')
        
        if not sequence:
            raise ValueError("Empty sequence")
            
        return f"{header}\n{sequence}"
    except Exception as e:
        raise ValueError(f"FASTA processing failed: {str(e)}") from e

def find_crispr_targets(sequence):
    """Identify CRISPR-Cas9 target sites with NGG PAM"""
    return [{
        'position': m.start(),
        'target': m.group(1)[:20],  # Capture 20bp before GG
        'pam': m.group(1)[-2:]
    } for m in CRISPR_PAM.finditer(sequence)]

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    stats = {'total': 0, 'valid': 0, 'errors': []}

    with open('flowering_genes_with_fasta.csv') as infile, \
         open(COMBINED_FASTA, 'w') as combined:
        
        reader = csv.DictReader(infile)
        
        for row in reader:
            stats['total'] += 1
            
            gene_id = row['gene_id_or_entry_id']
            symbol = row['symbol_or_gene'].strip()
            
            try:
                if not TARGET_PATTERNS.search(symbol):
                    continue
                    
                clean_fasta = process_fasta(row['fasta'])
                sequence = clean_fasta.split('\n', 1)[1]
                
                # Write individual gene file
                gene_file = OUTPUT_DIR / f"{gene_id}_{symbol}.fasta"
                with open(gene_file, 'w') as f:
                    f.write(clean_fasta)
                    
                # Add to combined file
                combined.write(f"{clean_fasta}\n\n")
                
                # Find CRISPR targets
                targets = find_crispr_targets(sequence)
                if targets:
                    target_file = gene_file.with_suffix('.crispr.txt')
                    with open(target_file, 'w') as f:
                        f.write(f"CRISPR targets for {gene_id} ({symbol}):\n")
                        for t in targets:
                            f.write(f"Position {t['position']}: {t['target']}{t['pam']}\n")
                
                stats['valid'] += 1
                
            except Exception as e:
                stats['errors'].append(f"Row {stats['total']} ({gene_id}): {str(e)}")
                
    print(f"Processed {stats['total']} genes")
    print(f"Successfully isolated {stats['valid']} sequences")
    print(f"Errors encountered: {len(stats['errors'])}")
    for error in stats['errors']:
        print(f" - {error}")

if __name__ == "__main__":
    main()