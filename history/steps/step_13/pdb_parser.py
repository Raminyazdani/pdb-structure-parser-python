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
    
    def hetero_atom_pdb_reader(self, pdb_file_path):
        """
        Read HETATM lines from PDB file
        """
        hetatom_lines = []
        try:
            with open(pdb_file_path, 'r') as f:
                for line in f:
                    if line.startswith('HETATM'):
                        hetatom_data = {
                            'record': line[0:6].strip(),
                            'serial': int(line[6:11].strip()),
                            'atom_name': line[12:16].strip(),
                            'res_name': line[17:20].strip(),
                            'chain': line[21:22].strip(),
                            'res_seq': int(line[22:26].strip()),
                            'x': float(line[30:38].strip()),
                            'y': float(line[38:46].strip()),
                            'z': float(line[46:54].strip()),
                        }
                        hetatom_lines.append(hetatom_data)
        except Exception as e:
            print(f"Error reading heteroatoms: {e}")
        return hetatom_lines
    
    def hetero_atom_residue_counter(self, heteroatom_lines):
        """
        Count unique heteroatom residues (excluding water)
        """
        residues = set()
        for atom in heteroatom_lines:
            res_name = atom['res_name']
            if res_name != 'HOH':  # Exclude water
                res_id = (atom['chain'], atom['res_seq'], res_name)
                residues.add(res_id)
        
        residue_counts = {}
        for res_id in residues:
            res_name = res_id[2]
            residue_counts[res_name] = residue_counts.get(res_name, 0) + 1
        
        return dict(sorted(residue_counts.items(), key=lambda x: x[1], reverse=True))
    
    def distance_calculator(self, x1, y1, z1, x2, y2, z2):
        """Calculate Euclidean distance between two points"""
        return ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)**0.5
    
    def most_distant_residue_finder(self, atom_lines):
        """Find the most distant residue pair"""
        # Get CA atoms for each residue
        ca_atoms = {}
        for atom in atom_lines:
            if atom['atom_name'] == 'CA':
                res_id = (atom['chain'], atom['res_seq'], atom['res_name'])
                ca_atoms[res_id] = (atom['x'], atom['y'], atom['z'])
        
        max_dist = 0
        max_pair = None
        
        ca_list = list(ca_atoms.items())
        for i in range(len(ca_list)):
            for j in range(i+1, len(ca_list)):
                res1, coord1 = ca_list[i]
                res2, coord2 = ca_list[j]
                dist = self.distance_calculator(coord1[0], coord1[1], coord1[2],
                                               coord2[0], coord2[1], coord2[2])
                if dist > max_dist:
                    max_dist = dist
                    max_pair = (res1, res2)
        
        return max_pair, max_dist
    
    def radius_of_gyration_calculator(self, atom_lines):
        """
        Calculate radius of gyration for the structure
        """
        # Atomic masses
        atomic_masses = {
            'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
            'S': 32.06, 'P': 30.974, 'FE': 55.845
        }
        
        # Calculate center of mass
        total_mass = 0
        cx, cy, cz = 0, 0, 0
        
        for atom in atom_lines:
            element = atom.get('element', '').strip().upper()
            mass = atomic_masses.get(element, 12.011)  # Default to carbon
            
            cx += atom['x'] * mass
            cy += atom['y'] * mass
            cz += atom['z'] * mass
            total_mass += mass
        
        cx /= total_mass
        cy /= total_mass
        cz /= total_mass
        
        # Calculate radius of gyration
        sum_sq_dist = 0
        for atom in atom_lines:
            element = atom.get('element', '').strip().upper()
            mass = atomic_masses.get(element, 12.011)
            
            dx = atom['x'] - cx
            dy = atom['y'] - cy
            dz = atom['z'] - cz
            
            sum_sq_dist += mass * (dx**2 + dy**2 + dz**2)
        
        rg = (sum_sq_dist / total_mass) ** 0.5
        return rg



    def amino_acid_hydrophobicity_composition_calculator(self, amino_acid_composition):
        """
        Calculate hydrophobic vs hydrophilic amino acid composition
        Uses Kyte-Doolittle hydrophobicity scale
        """
        Kyte_Doolittle_scale = {
            'ILE': 4.5, 'VAL': 4.2, 'LEU': 3.8, 'PHE': 2.8, 'CYS': 2.5,
            'MET': 1.9, 'ALA': 1.8, 'GLY': -0.4, 'THR': -0.7, 'SER': -0.8,
            'TRP': -0.9, 'TYR': -1.3, 'PRO': -1.6, 'HIS': -3.2, 'GLU': -3.5,
            'GLN': -3.5, 'ASP': -3.5, 'ASN': -3.5, 'LYS': -3.9, 'ARG': -4.5
        }
        
        hydrophobic_count = 0
        hydrophilic_count = 0
        
        for aa, count in amino_acid_composition.items():
            if aa in Kyte_Doolittle_scale:
                if Kyte_Doolittle_scale[aa] > 0:
                    hydrophobic_count += count
                else:
                    hydrophilic_count += count
        
        return {'hydrophobic': hydrophobic_count, 'hydrophilic': hydrophilic_count}
    
    def amino_acid_charge_composition_calculator(self, amino_acid_composition):
        """
        Calculate charged amino acid composition (positive vs negative)
        """
        positive_charged = {'LYS', 'ARG', 'HIS'}
        negative_charged = {'ASP', 'GLU'}
        
        positive_count = sum(count for aa, count in amino_acid_composition.items() if aa in positive_charged)
        negative_count = sum(count for aa, count in amino_acid_composition.items() if aa in negative_charged)
        
        return {'positive': positive_count, 'negative': negative_count}
    
    def atomic_composition_calculator(self, atom_lines):
        """
        Calculate atomic composition (C, N, O, S counts)
        """
        atoms = {}
        for atom in atom_lines:
            element = atom.get('element', '').strip()
            if element:
                atoms[element] = atoms.get(element, 0) + 1
        
        # Sort by frequency
        sorted_atoms = dict(sorted(atoms.items(), key=lambda x: x[1], reverse=True))
        return sorted_atoms
    
    def atomic_composition_percentage_calculator(self, atom_lines):
        """
        Calculate atomic composition percentages
        """
        composition = self.atomic_composition_calculator(atom_lines)
        total = sum(composition.values())
        percentages = {elem: (count / total * 100) for elem, count in composition.items()}
        sorted_percentages = dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))
        return sorted_percentages
    
    def hetero_atom_pdb_reader(self, pdb_file_path):
        """
        Read HETATM lines from PDB file
        """
        hetatom_lines = []
        try:
            with open(pdb_file_path, 'r') as f:
                for line in f:
                    if line.startswith('HETATM'):
                        hetatom_data = {
                            'record': line[0:6].strip(),
                            'serial': int(line[6:11].strip()),
                            'atom_name': line[12:16].strip(),
                            'res_name': line[17:20].strip(),
                            'chain': line[21:22].strip(),
                            'res_seq': int(line[22:26].strip()),
                            'x': float(line[30:38].strip()),
                            'y': float(line[38:46].strip()),
                            'z': float(line[46:54].strip()),
                        }
                        hetatom_lines.append(hetatom_data)
        except Exception as e:
            print(f"Error reading heteroatoms: {e}")
        return hetatom_lines
    
    def hetero_atom_residue_counter(self, heteroatom_lines):
        """
        Count unique heteroatom residues (excluding water)
        """
        residues = set()
        for atom in heteroatom_lines:
            res_name = atom['res_name']
            if res_name != 'HOH':  # Exclude water
                res_id = (atom['chain'], atom['res_seq'], res_name)
                residues.add(res_id)
        
        residue_counts = {}
        for res_id in residues:
            res_name = res_id[2]
            residue_counts[res_name] = residue_counts.get(res_name, 0) + 1
        
        return dict(sorted(residue_counts.items(), key=lambda x: x[1], reverse=True))
    
    def distance_calculator(self, x1, y1, z1, x2, y2, z2):
        """Calculate Euclidean distance between two points"""
        return ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)**0.5
    
    def most_distant_residue_finder(self, atom_lines):
        """Find the most distant residue pair"""
        # Get CA atoms for each residue
        ca_atoms = {}
        for atom in atom_lines:
            if atom['atom_name'] == 'CA':
                res_id = (atom['chain'], atom['res_seq'], atom['res_name'])
                ca_atoms[res_id] = (atom['x'], atom['y'], atom['z'])
        
        max_dist = 0
        max_pair = None
        
        ca_list = list(ca_atoms.items())
        for i in range(len(ca_list)):
            for j in range(i+1, len(ca_list)):
                res1, coord1 = ca_list[i]
                res2, coord2 = ca_list[j]
                dist = self.distance_calculator(coord1[0], coord1[1], coord1[2],
                                               coord2[0], coord2[1], coord2[2])
                if dist > max_dist:
                    max_dist = dist
                    max_pair = (res1, res2)
        
        return max_pair, max_dist
    
    def radius_of_gyration_calculator(self, atom_lines):
        """
        Calculate radius of gyration for the structure
        """
        # Atomic masses
        atomic_masses = {
            'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
            'S': 32.06, 'P': 30.974, 'FE': 55.845
        }
        
        # Calculate center of mass
        total_mass = 0
        cx, cy, cz = 0, 0, 0
        
        for atom in atom_lines:
            element = atom.get('element', '').strip().upper()
            mass = atomic_masses.get(element, 12.011)  # Default to carbon
            
            cx += atom['x'] * mass
            cy += atom['y'] * mass
            cz += atom['z'] * mass
            total_mass += mass
        
        cx /= total_mass
        cy /= total_mass
        cz /= total_mass
        
        # Calculate radius of gyration
        sum_sq_dist = 0
        for atom in atom_lines:
            element = atom.get('element', '').strip().upper()
            mass = atomic_masses.get(element, 12.011)
            
            dx = atom['x'] - cx
            dy = atom['y'] - cy
            dz = atom['z'] - cz
            
            sum_sq_dist += mass * (dx**2 + dy**2 + dz**2)
        
        rg = (sum_sq_dist / total_mass) ** 0.5
        return rg









def print_function(pdb_file):
    """
    Main function to analyze PDB file and print all results
    """
    parser = RaminCalc()
    
    print(f"\nAnalyzing PDB file: {pdb_file}\n")
    print("="*60)
    
    # Read ATOM lines
    atoms = parser.pdb_file_reader(pdb_file)
    print(f"\nTotal ATOM records: {len(atoms)}")
    
    # Amino acid composition
    aa_comp = parser.amino_acid_composition_calculator(atoms)
    print("\nAmino Acid Composition:")
    for aa, count in aa_comp.items():
        print(f"  {aa}: {count}")
    
    # Amino acid percentages
    aa_pct = parser.amino_acid_composition_percentage_calculator(atoms)
    print("\nAmino Acid Percentages:")
    for aa, pct in aa_pct.items():
        print(f"  {aa}: {pct:.2f}%")
    
    # Hydrophobicity
    hydro = parser.amino_acid_hydrophobicity_composition_calculator(aa_comp)
    print(f"\nHydrophobicity: Hydrophobic={hydro['hydrophobic']}, Hydrophilic={hydro['hydrophilic']}")
    
    # Charge composition
    charge = parser.amino_acid_charge_composition_calculator(aa_comp)
    print(f"\nCharge: Positive={charge['positive']}, Negative={charge['negative']}")
    
    # Atomic composition
    atomic = parser.atomic_composition_calculator(atoms)
    print("\nAtomic Composition:")
    for elem, count in atomic.items():
        print(f"  {elem}: {count}")
    
    # Heteroatoms
    heteroatoms = parser.hetero_atom_pdb_reader(pdb_file)
    hetero_res = parser.hetero_atom_residue_counter(heteroatoms)
    print(f"\nHeteroatom residues: {hetero_res}")
    
    # Spatial metrics
    pair, dist = parser.most_distant_residue_finder(atoms)
    if pair:
        print(f"\nMost distant residues: {pair[0]} - {pair[1]}, Distance: {dist:.2f} Å")
    
    rg = parser.radius_of_gyration_calculator(atoms)
    print(f"Radius of gyration: {rg:.2f} Å")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print_function(sys.argv[1])
    else:
        print("Usage: python pdb_parser.py <pdb_file>")

