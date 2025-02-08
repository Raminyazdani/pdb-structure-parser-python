"""
PDB Parser for Structural Bioinformatics
"""

class RaminCalc:
    """Main class for PDB file parsing and calculations"""
    
    def __init__(self):
        """Initialize the parser"""
        pass
    
    def pdb_file_reader(self, pdb_file_path):
        """
        Read ATOM lines from a PDB file
        
        Args:
            pdb_file_path: Path to the PDB file
            
        Returns:
            list: List of ATOM line dictionaries
        """
        atom_lines = []
        try:
            with open(pdb_file_path, 'r') as f:
                for line in f:
                    if line.startswith('ATOM'):
                        # Parse ATOM line using PDB format specification
                        atom_data = {
                            'record': line[0:6].strip(),
                            'serial': int(line[6:11].strip()),
                            'atom_name': line[12:16].strip(),
                            'res_name': line[17:20].strip(),
                            'chain': line[21:22].strip(),
                            'res_seq': int(line[22:26].strip()),
                            'x': float(line[30:38].strip()),
                            'y': float(line[38:46].strip()),
                            'z': float(line[46:54].strip()),
                            'element': line[76:78].strip()
                        }
                        atom_lines.append(atom_data)
        except FileNotFoundError:
            print(f"Error: File {pdb_file_path} not found")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        return atom_lines
    
    def amino_acid_composition_calculator(self, atom_lines):
        """
        Calculate amino acid composition from ATOM records
        
        Args:
            atom_lines: List of ATOM line dictionaries
            
        Returns:
            dict: Amino acid composition (sorted by frequency)
        """
        residues = {}
        seen_residues = set()
        
        for atom in atom_lines:
            residue_id = (atom['chain'], atom['res_seq'], atom['res_name'])
            if residue_id not in seen_residues:
                res_name = atom['res_name']
                residues[res_name] = residues.get(res_name, 0) + 1
                seen_residues.add(residue_id)
        
        # Sort by frequency (descending)
        sorted_residues = dict(sorted(residues.items(), key=lambda x: x[1], reverse=True))
        return sorted_residues
    
    def amino_acid_composition_percentage_calculator(self, atom_lines):
        """
        Calculate amino acid composition percentages
        
        Args:
            atom_lines: List of ATOM line dictionaries
            
        Returns:
            dict: Amino acid percentages (sorted by percentage)
        """
        composition = self.amino_acid_composition_calculator(atom_lines)
        total = sum(composition.values())
        
        # Fixed: Multiply by 100 for percentage
        percentages = {aa: (count / total * 100) for aa, count in composition.items()}
        
        # Sort by percentage (descending)
        sorted_percentages = dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))
        return sorted_percentages


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        parser = RaminCalc()
        atoms = parser.pdb_file_reader(sys.argv[1])
        print(f"Read {len(atoms)} ATOM records")
        
        composition = parser.amino_acid_composition_calculator(atoms)
        print("\nAmino Acid Composition:")
        for aa, count in composition.items():
            print(f"  {aa}: {count}")
        
        percentages = parser.amino_acid_composition_percentage_calculator(atoms)
        print("\nAmino Acid Percentages:")
        for aa, pct in percentages.items():
            print(f"  {aa}: {pct:.2f}%")
