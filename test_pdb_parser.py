import pytest
from pdb_parser import (
    pdb_file_reader,
    amino_acid_composition_calculator,
    amino_acid_composition_percentage_calculator,
    atomic_composition_calculator,
    atomic_composition_percentage_calculator,
    amino_acid_hydrophobicity_composition_calculator,
    amino_acid_hydrophobicity_composition_percentage_calculator,
    amino_acid_charge_composition_calculator,
    hetero_atom_pdb_reader,
    hetero_atom_residue_counter,
    most_distant_residue_finder,
    radius_of_gyration_calculator,
    Kyte_Doolittle_scale
)
import os

# Sample PDB data for testing
pdb_content = """
ATOM      1  N   MET A   1      38.428  13.947  27.340  1.00 54.69           N  
ATOM      2  CA  MET A   1      37.200  14.748  27.740  1.00 54.69           C  
ATOM      3  C   MET A   1      36.000  13.800  27.340  1.00 54.69           C  
ATOM      4  O   MET A   1      35.000  14.200  27.740  1.00 54.69           O  
ATOM      5  CB  MET A   1      37.000  15.000  29.200  1.00 54.69           C  
ATOM      6  N   GLY A   2      36.000  12.600  26.940  1.00 54.69           N  
ATOM      7  CA  GLY A   2      34.800  11.800  26.540  1.00 54.69           C  
ATOM      8  C   GLY A   2      33.600  12.600  26.940  1.00 54.69           C  
ATOM      9  O   GLY A   2      32.600  12.200  26.540  1.00 54.69           O
ATOM     10  O   GLY A   2      32.600  12.200  26.540  1.00 54.69           O  
HETATM   11  O   ABC A   3      31.600  11.200  26.140  1.00 54.69           O  
HETATM   12  C   ABC A   3      32.600  11.200  26.140  1.00 54.69           C 
HETATM   13  B   BLA A   4      33.600  11.200  26.140  1.00 54.69           B 
"""

@pytest.fixture
def create_pdb_file(tmp_path):
    pdb_file = tmp_path / "test.pdb"
    pdb_file.write_text(pdb_content)
    return pdb_file

def test_pdb_file_reader(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    assert len(atom_lines) == 10 

def test_amino_acid_composition_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    composition = amino_acid_composition_calculator(atom_lines)
    assert composition == {'MET': 1, 'GLY': 1}

def test_amino_acid_composition_percentage_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    percentage = amino_acid_composition_percentage_calculator(atom_lines)
    assert percentage == {'MET': 50.0, 'GLY': 50.0}

def test_atomic_composition_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    composition = atomic_composition_calculator(atom_lines)
    assert composition == {'N': 2, 'C': 5, 'O': 3}

def test_atomic_composition_percentage_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    percentage = atomic_composition_percentage_calculator(atom_lines)
    assert percentage == {'N': 20.0, 'C': 50.0, 'O': 30.0}

def test_amino_acid_hydrophobicity_composition_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    composition = amino_acid_composition_calculator(atom_lines)
    hydrophobicity = amino_acid_hydrophobicity_composition_calculator(composition, Kyte_Doolittle_scale)
    assert hydrophobicity == {'Hydrophobic': 1, 'Hydrophilic': 1}

def test_amino_acid_hydrophobicity_composition_percentage_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    composition = amino_acid_composition_calculator(atom_lines)
    percentage = amino_acid_hydrophobicity_composition_percentage_calculator(composition, Kyte_Doolittle_scale)
    assert percentage == {'Hydrophobic': 50.0, 'Hydrophilic': 50.0}

def test_amino_acid_charge_composition_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    composition = amino_acid_composition_calculator(atom_lines)
    charge = amino_acid_charge_composition_calculator(composition)
    assert charge == {'Positive': 0, 'Negative': 0}

def test_hetero_atom_pdb_reader(create_pdb_file):
    pdb_file = create_pdb_file
    heteroatom_lines = hetero_atom_pdb_reader(str(pdb_file))
    assert len(heteroatom_lines) == 3  # 3 HETATM line in the sample PDB content

def test_hetero_atom_residue_counter(create_pdb_file):
    pdb_file = create_pdb_file
    heteroatom_lines = hetero_atom_pdb_reader(str(pdb_file))
    composition = hetero_atom_residue_counter(heteroatom_lines)
    assert composition == {'ABC': 1, 'BLA': 1}

def test_most_distant_residue_finder(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    most_distant = most_distant_residue_finder(atom_lines)
    assert most_distant == (('1', '2'), pytest.approx(4.0, 0.3))  # Approximate distance

def test_radius_of_gyration_calculator(create_pdb_file):
    pdb_file = create_pdb_file
    atom_lines = pdb_file_reader(str(pdb_file))
    radius_of_gyration = radius_of_gyration_calculator(atom_lines)
    assert radius_of_gyration == pytest.approx(2.3, 0.3) 