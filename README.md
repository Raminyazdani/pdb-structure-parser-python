# Protein Structure Parsing and Analysis

**PDB file parsing and structural bioinformatics analysis**

**Stack:** Python, BioPython

## Overview

This project implements a comprehensive PDB (Protein Data Bank) file parser and structural analysis toolkit. It extracts and analyzes various structural properties of proteins including amino acid composition, atomic statistics, spatial measurements, and structural characteristics from PDB format files.

## Problem & Approach

**Problem:** Parse and analyze protein 3D structure data from PDB files to extract meaningful structural and compositional information.

**Approach:**
- Implement custom PDB file parser (without external parsing libraries)
- Calculate amino acid composition and categorization
- Compute atomic statistics (C, N, O, S counts)
- Identify heteroatoms and ligands
- Calculate spatial metrics (inter-residue distances, radius of gyration)
- Analyze charge distribution across residues

## Tech Stack

- **Python 3.x** - Core programming language
- **Standard library only** - No external parsing dependencies for core functionality
- **BioPython** (optional) - For validation and comparison

## Folder Structure

```
raya00001_7068679-assignment1/
├── assignment1_template.py    # Main PDB parser implementation
├── test_assignment1.py        # Test suite for validation
├── results.txt                # Example output results
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup / Installation

1. **Ensure Python 3.x is installed**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## How to Run

1. **Navigate to project directory:**
```bash
cd raya00001_7068679-assignment1
```

2. **Run the parser:**
```bash
python assignment1_template.py
```

3. **Run tests:**
```bash
python test_assignment1.py
```

## Data / Inputs

**Input Files:**
- PDB structure files (e.g., `1FCN.pdb` - Ficolin protein structure)
- Any valid PDB format file from RCSB Protein Data Bank

**Data Source:**
- Download from RCSB PDB: https://www.rcsb.org/
- Example: Biological assembly 1 of PDB ID 1FCN

**Data Location:** Place PDB files in project directory or specify path in script

## Outputs

**Analysis Results:**

1. **Amino Acid Composition:** Counts and percentages, sorted by frequency
2. **Hydrophobicity Analysis:** Based on Kyte-Doolittle scale
3. **Atomic Composition:** Statistics for C, N, O, S atoms
4. **Charge Analysis:** Positive and negative charged residues
5. **Heteroatom Identification:** Non-standard residues (excluding water)
6. **Spatial Metrics:** Max distance between residues, radius of gyration

**Output Format:** Text file with formatted statistics and measurements

## Reproducibility Notes

- Parser uses only standard Python libraries
- Deterministic calculations (no randomness)
- Tested with multiple PDB files for robustness
- All file paths should be relative or configurable
- Originally created in an academic setting

## Troubleshooting

- **File not found:** Ensure PDB file is in correct directory
- **Parse errors:** Verify PDB file format validity
- **Import errors:** Install dependencies with `pip install -r requirements.txt`

## Notes

- Originally created in an academic setting
- Parser handles standard PDB format
- Radius of gyration indicates structural compactness
- Kyte-Doolittle scale for hydrophobicity classification
- Comprehensive test suite included
