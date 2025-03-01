import sys
import math
from tempfile import template

"""
PDB Parser for Structural Bioinformatics
"""

Kyte_Doolittle_scale = {'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5, 'CYS': 2.5,
                        'GLN': -3.5, 'GLU': -3.5, 'GLY': -0.4, 'HIS': -3.2, 'ILE': 4.5,
                        'LEU': 3.8, 'LYS': -3.9, 'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6,
                        'SER': -0.8, 'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2}


class RaminCalc:
    # Base self designed Class for implementing statics method for extracting relevant data from PDB lines


    @staticmethod
    def get_data_pdb(pdb_line, items=None):
        # this function get a single pdb_line and the items is not mandatory
        # if items is None or not given it will return all the data according to the pdb file format documentation


        # this is template for key values stores in each pdb line ATOM and HETATM
        template_columns = {
            "Type": pdb_line[0:6].strip(),
            "Atom serial number": pdb_line[6:11].strip(),
            "Atom name": pdb_line[12:16].strip(),
            "Alternate location indicator": pdb_line[16].strip(),
            "Residue name": pdb_line[17:20].strip(),
            "Chain identifier": pdb_line[21].strip(),
            "Residue sequence number": pdb_line[22:26].strip(),
            "Code for insertions of residues": pdb_line[26].strip(),
            "X orthogonal Å coordinate": pdb_line[30:38].strip(),
            "Y orthogonal Å coordinate": pdb_line[38:46].strip(),
            "Z orthogonal Å coordinate": pdb_line[46:54].strip(),
            "Occupancy": pdb_line[54:60].strip(),
            "Temperature factor": pdb_line[60:66].strip(),
            "Segment identifier": pdb_line[72:76].strip(),
            "Element symbol": pdb_line[76:78].strip(),
            "Charge": pdb_line[78:80].strip(),
        }

        # return all extracted data from line
        if items is None:
            return template_columns

        # if items given to function it returns the desired items only in format of dictionary
        return_temp = {}
        for item in items:
            if item in template_columns.keys():
                return_temp[item] = template_columns[item]
        return return_temp

    @staticmethod
    def get_custom_data_pdb(pdb_line, template_get, simple=False):

        # get custom template design in arguments and accordingly extract the data from the pdb_line
        result_temp = "{"
        for key, value in template_get.items():
            result_temp += "'" + key + "'" + ":pdb_line" + str(value) + ",\n"
        result_temp += "}"

        # for one time evaluating , the result temp is string formated command for creating a dictionary
        result_temp = eval(result_temp)

        # if simple argument TRUE given to the function , instead of returning the dictionary it will only return the data value extracted
        # if there are multiple items in template to get from pdb lines , it will not return single data
        if simple == True and len(result_temp.items()) == 1:
            return list(result_temp.values())[0]
        return result_temp

    @staticmethod
    def get_template_pdb(items):

        # this is a function to generate a string template only for get_custom_data_pdb staticmethod for further eval() inside that function
        # it gets a list of items and returns the dictionary converted to key,value format of the pdb line docs
        template_columns = {
            "Type": "[0:6].strip()",
            "Atom serial number": "[6:11].strip()",
            "Atom name": "[12:16].strip()",
            "Alternate location indicator": "[16].strip()",
            "Residue name": "[17:20]",
            "Chain identifier": "[21].strip()",
            "Residue sequence number": "[22:26].strip()",
            "Code for insertions of residues": "[26].strip()",
            "X orthogonal Å coordinate": "[30:38].strip()",
            "Y orthogonal Å coordinate": "[38:46].strip()",
            "Z orthogonal Å coordinate": "[46:54].strip()",
            "Occupancy": "[54:60].strip()",
            "Temperature factor": "[60:66].strip()",
            "Segment identifier": "[72:76].strip()",
            "Element symbol": "[76:78].strip()",
            "Charge": "[78:80].strip()",
        }
        return_temp = {}
        for item in items:
            if item in template_columns.keys():
                return_temp[item] = template_columns[item]
        return return_temp


def pdb_file_reader(pdb_file):
    """
        Function to read PDB files

        Parameters
        ----------
        pdb_file : str
            path to pdb file

        Return
        ----------
        atom_lines : list
            list of atomic lines

    """

    atom_lines = []

    with open(pdb_file, "r") as f:
        for line in f.readlines():
            if line.startswith("ATOM"):
                atom_lines.append(line.strip())
    return atom_lines


def amino_acid_composition_calculator(atom_lines):
    """
        Function to find amino acid composition

        Parameters
        ----------
        atom_lines : str
            list of atomic lines

        Return
        ----------
        amino_acid_composition : dictionary
            dictionary of amino acid composition 
            key: amino acid 3-letter code etc: ARG
            value: how many times observed (int)

    """

    amino_acid_composition = {}

    # needed columns to generate template from
    needed_cols_temp = ["Residue name", "Residue sequence number"]
    # generating a template for my RaminCalc statics method class
    temp_template = RaminCalc.get_template_pdb(needed_cols_temp)

    for line in atom_lines:
        # parsing the template for each line to get the desired data from each line
        data = RaminCalc.get_custom_data_pdb(line, temp_template)
        # creating a key equal to Residue name and values are storing in a list format and stores the Residue sequence number for further removing the duplicates
        amino_acid_composition[data["Residue name"]] = amino_acid_composition.get(data["Residue name"], []) + [
            data["Residue sequence number"]]
    # removing duplicates and count each residue
    for key, value in amino_acid_composition.items():
        amino_acid_composition[key] = len(set(value))
    return dict(sorted(amino_acid_composition.items(),key=lambda x: x[1], reverse=True))


def amino_acid_composition_percentage_calculator(atom_lines):
    """
        Function to find amino acid composition percentage

        Parameters
        ----------
        atom_lines : str
            list of atomic lines

        Return
        ----------
        amino_acid_composition_percentage : dictionary
            dictionary of amino acid composition 
            key: amino acid 3-letter code etc: ARG
            value: how many percent it is observed in the structure

    """

    amino_acid_composition_percentage = {}

    # getting count data from previous method
    amino_acid_composition = amino_acid_composition_calculator(atom_lines)

    # getting a sum of all for further division
    sum_all = sum(amino_acid_composition.values())

    # devide each count / all_counts for getting the percentage
    for key, value in amino_acid_composition.items():
        amino_acid_composition_percentage[key] = value * 100 / sum_all

    return dict(sorted(amino_acid_composition_percentage.items(),key=lambda x: x[1], reverse=True))


def atomic_composition_calculator(atom_lines):
    """
        Function to find atomic composition

        Parameters
        ----------
        atom_lines : str
            list of atomic lines

        Return
        ----------
        atomic_composition : dictionary
            dictionary of atomic composition 
            key: Atomic code etc: C, O, N
            value: how many times observed (int)

    """

    atomic_composition = {}

    # defining which columns we need
    needed_cols_temp = ["Element symbol"]
    # generating a template for needed columns
    temp_template = RaminCalc.get_template_pdb(needed_cols_temp)
    for line in atom_lines:
        # extract only the ELEMENT symbol which is atomic code and count the occurrence
        data = RaminCalc.get_custom_data_pdb(line, temp_template, True)
        atomic_composition[data] = atomic_composition.get(data, 0) + 1
    return dict(sorted(atomic_composition.items(),key=lambda x: x[1], reverse=True))


def atomic_composition_percentage_calculator(atom_lines):
    """
        Function to find atomic composition percentage

        Parameters
        ----------
        atom_lines : str
            list of atomic lines

        Return
        ----------
        atomic_composition_percentage : dictionary
            dictionary of atomic composition 
            key: Atomic code etc: C, O, N
            value: how many percent it is observed

    """

    atomic_composition_percentage = {}
    # getting counts from previous function
    atomic_composition = atomic_composition_calculator(atom_lines)

    # count all atoms
    sum_all = sum(atomic_composition.values())

    # calculate the percentage
    for key, value in atomic_composition.items():
        atomic_composition_percentage[key] = value * 100 / sum_all

    return dict(sorted(atomic_composition_percentage.items(),key=lambda x: x[1], reverse=True))


def amino_acid_hydrophobicity_composition_calculator(amino_acid_composition, Kyte_Doolittle_scale):
    """
        Function to find amino acid hydrophobicity composition

        Parameters
        ----------
        amino_acid_composition : dictionary
            dictionary of atomic composition 
            key: 3 letter amino acid code etc: ARG
            value: how many times observed (int)
        
        Kyte_Doolittle_scale : dictionary
            dictionary of kyte doolittle hydrophobicity values

        Return
        ----------
        amino_acid_hydrophobicity_composition : dictionary
            dictionary of amino acid hydrophobicity composition 
            key: Hydrophobic and Hydrophilic
            value: how many times observed (int)

    """
    new_kyte = {}

    # for easier approach , translate the Kyte_Doolittle_scale values to "Hydrophilic" and "Hydrophobic"
    for k, v in Kyte_Doolittle_scale.items():
        new_kyte[k] = "Hydrophobic" if v > 0 else "Hydrophilic"


    amino_acid_hydrophobicity_composition = {"Hydrophobic": 0, "Hydrophilic": 0}

    # value is count of keys which keys are amino acid names , by count of them Hydrophobic or Hydrophilic increments
    for key, value in amino_acid_composition.items():
        amino_acid_hydrophobicity_composition[new_kyte[key]] += value

    return amino_acid_hydrophobicity_composition


def amino_acid_hydrophobicity_composition_percentage_calculator(amino_acid_composition, Kyte_Doolittle_scale):
    """
        Function to find amino acid hydrophobicity composition percentage

        Parameters
        ----------
        amino_acid_composition : dictionary
            dictionary of atomic composition 
            key: 3 letter amino acid code etc: ARG
            value: how many times observed (int)
        
        Kyte_Doolittle_scale : dictionary
            dictionary of kyte doolittle hydrophobicity values

        Return
        ----------
        amino_acid_hydrophobicity_composition_percentage : dictionary
            dictionary of amino acid hydrophobicity composition 
            key: Hydrophobic and Hydrophilic
            value: how many percentage it is observed

    """

    amino_acid_hydrophobicity_composition_percentage = {"Hydrophobic": 0, "Hydrophilic": 0}

    # get the data from previous function
    amino_acid_hydrophobicity_composition = amino_acid_hydrophobicity_composition_calculator(amino_acid_composition,
                                                                                             Kyte_Doolittle_scale)
    # count all for futher calculation
    sum_temp = sum(amino_acid_hydrophobicity_composition.values())

    # calculate the percentage
    amino_acid_hydrophobicity_composition_percentage["Hydrophobic"] = amino_acid_hydrophobicity_composition[
                                                                          "Hydrophobic"] * 100 / sum_temp
    amino_acid_hydrophobicity_composition_percentage["Hydrophilic"] = amino_acid_hydrophobicity_composition[
                                                                          "Hydrophilic"] * 100 / sum_temp

    return amino_acid_hydrophobicity_composition_percentage


def amino_acid_charge_composition_calculator(amino_acid_composition):
    """
        Function to find amino acid charge composition

        Parameters
        ----------
        amino_acid_composition : dictionary
            dictionary of atomic composition 
            key: 3 letter amino acid code etc: ARG
            value: how many times observed (int)
        
        Return
        ----------
        amino_acid_charge_composition : dictionary
            dictionary of amino acid charge composition 
            key: Positive or Negative
            value: how many times observed (int)

    """

    """
    
    Positively charged amino acids: Lysine, Arginine, Histidine
    Negatively charged amino acids: Aspartate, Glutamate

    """

    amino_acid_charge_composition = {"Positive": 0, "Negative": 0}


    # straight forward if statements , if the amino acid charge is + increment the Positivie in Dict
    # otherwise if its negative , increments the negative
    for k, v in amino_acid_composition.items():
        if k in ["LYS", "ARG", "HIS"]:
            amino_acid_charge_composition["Positive"] += v
        elif k in ["ASP", "GLU"]:
            amino_acid_charge_composition["Negative"] += v

    return amino_acid_charge_composition


def hetero_atom_pdb_reader(pdb_file):
    """
        Function to read PDB files and return heteroatom lines

        Parameters
        ----------
        pdb_file : str
            path to pdb file

        Return
        ----------
        heteroatom_lines : list
            list of heteroatom lines

    """

    heteroatom_lines = []
    # reading heteroatom lines like reading the ATOM lines
    # criteria is starting of the line
    with open(pdb_file, "r") as f:
        for line in f.readlines():
            if line.startswith("HETATM") and line[17:20]!="HOH":
                heteroatom_lines.append(line.strip())

    return heteroatom_lines


def hetero_atom_residue_counter(heteroatom_lines):
    """
        Function to count heteroatom residues

        Parameters
        ----------
        heteroatom_lines : list
            list of heteroatom lines

        Return
        ----------
        hetero_atom_composition : dictionary
            dictionary of heteroatoms
            key: residue name
            value: count (int)
        

    """

    hetero_atom_composition = {}

    needed_cols_temp = ["Residue name", "Residue sequence number"]
    # generating a template for my RaminCalc statics method class
    temp_template = RaminCalc.get_template_pdb(needed_cols_temp)

    for line in heteroatom_lines:
        # parsing the template for each line to get the desired data from each line
        data = RaminCalc.get_custom_data_pdb(line, temp_template)
        # creating a key equal to Residue name and values are storing in a list format and stores the Residue sequence number for further removing the duplicates
        hetero_atom_composition[data["Residue name"]] = hetero_atom_composition.get(data["Residue name"], []) + [
            data["Residue sequence number"]]
    # removing duplicates and count each residue
    for key, value in hetero_atom_composition.items():
        hetero_atom_composition[key] = len(set(value))

    return hetero_atom_composition


def distance_calculator(x1, y1, z1, x2, y2, z2):
    x1, y1, z1, x2, y2, z2 = float(x1), float(y1), float(z1), float(x2), float(y2), float(z2)
    distance = math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)) + ((z2 - z1) * (z2 - z1)))

    return distance


def most_distant_residue_finder(atom_lines):
    """
        Function to find amino acid composition

        Parameters
        ----------
        atom_lines : str
            list of atomic lines

        Return
        ----------
        most_distant_residues : tuple
            tuple of most distant residues

    """

    groups = {}
    # select needed columns for further process
    temp_data_get = ["Chain identifier", "Atom name", "Residue sequence number", "X orthogonal Å coordinate",
                     "Y orthogonal Å coordinate", "Z orthogonal Å coordinate"]
    # generate the template needed for required columns
    temp_template = RaminCalc.get_template_pdb(temp_data_get)
    for l in atom_lines:
        data_temp = RaminCalc.get_custom_data_pdb(l, temp_template)

        # grouping the chains with their CA storing in values alongside X,Y,Z
        if data_temp["Chain identifier"] not in groups:
            groups[data_temp["Chain identifier"]] = []
        if data_temp["Atom name"] == "CA":
            groups[data_temp["Chain identifier"]].append(
                {"number": data_temp["Residue sequence number"], "X": data_temp["X orthogonal Å coordinate"],
                 "Y": data_temp["Y orthogonal Å coordinate"], "Z": data_temp["Z orthogonal Å coordinate"]})

    resid_1 = None
    resid_2 = None
    distance = None

    # calculating distance for each group
    for chain, CAs in groups.items():
        # if there are fewer CA than 2 , it will continue
        if len(CAs) >= 2:
            for i in range(len(CAs)):
                for j in range(i + 1, len(CAs)):
                    distance_temp = distance_calculator(CAs[i]["X"], CAs[i]["Y"], CAs[i]["Z"], CAs[j]["X"], CAs[j]["Y"],
                                                        CAs[j]["Z"])

                    # first attempt to set resid_1 and resid_2 and distance since the initial state is NONE
                    if distance is None:
                        resid_1 = CAs[i]["number"]
                        resid_2 = CAs[j]["number"]
                        distance = distance_temp
                        continue
                    # maximum distance criteria check
                    if distance_temp > distance:
                        resid_1 = CAs[i]["number"]
                        resid_2 = CAs[j]["number"]
                        distance = distance_temp

    # resid_1 = residue id of most distance residue #1
    # resid_2 = residue id of most distance residue #2
    # distance = distance between them
    # PS: Order of residue numbers does not matter both is accepted, explanation:
    # ((11,64),340) == ((64,11),340)

    most_distant_residues = ((resid_1, resid_2), distance)

    return most_distant_residues


### Bonus Point
def radius_of_gyration_calculator(atom_lines):
    """
        Function to find amino acid composition

        Parameters
        ----------
        atom_lines : str
            list of atomic lines

        Return
        ----------
        radius_of_gyration : float
            radius of gyration value of protein

    """
    # the Radius of gyration explanation :
    # The radius of gyration (Rg) of a protein's three-dimensional structure measures how its atoms are distributed around its axis
    # it quentify the compatness of  the protein's overally
    # lower Rg value: tightly packed, stable, well-folded protein structure
    # higher Rg value: more expanded , less compact [ due to unfolding, denaturation, or flexible regions].
    # RG provides insights into the protein's structural integrity, folding state, and any conformational changes,
    # RG is  essential for understanding protein behavior, stability
    # RG is essential for thes too : interactions with ligands or environmental factors


    radius_of_gyration = 0.0


    # for calculation of radius of gyraction first we need to find the center of mass of our protein
    mass = {"H": 1.00794, "He": 4.00260, "Li": 6.94100, "Be": 9.01218, "B": 10.81100,
            "C": 12.01070, "N": 14.00670, "O": 15.99940, "F": 18.99840, "Ne": 20.17970,
            "Na": 22.98977, "Mg": 24.30500, "Al": 26.98154, "Si": 28.08550, "P": 30.97376,
            "S": 32.06500, "Cl": 35.45300, "Ar": 39.94800, "K": 39.09830, "Ca": 40.07800,
            "Sc": 44.95591, "Ti": 47.86700, "V": 50.94150, "Cr": 51.99610, "Mn": 54.93805,
            "Fe": 55.84500, "Co": 58.93320, "Ni": 58.69340, "Cu": 63.54600, "Zn": 65.40900,
            "Ga": 69.72300, "Ge": 72.64000, "As": 74.92160, "Se": 78.96000, "Br": 79.90400,
            "Kr": 83.79800, "Rb": 85.46780, "Sr": 87.62000, "Y": 88.90585, "Zr": 91.22400,
            "Nb": 92.90638, "Mo": 95.94000, "Tc": 98.00000, "Ru": 101.07000, "Rh": 102.90550,
            "Pd": 106.42000, "Ag": 107.86820, "Cd": 112.41100, "In": 114.81800, "Sn": 118.71000,
            "Sb": 121.76000, "Te": 127.60000, "I": 126.90447, "Xe": 131.29300, "Cs": 132.90545,
            "Ba": 137.32700, "La": 138.90550, "Ce": 140.11600, "Pr": 140.90765, "Nd": 144.24000,
            "Pm": 145.00000, "Sm": 150.36000, "Eu": 151.96400, "Gd": 157.25000, "Tb": 158.92534,
            "Dy": 162.50000, "Ho": 164.93032, "Er": 167.25900, "Tm": 168.93421, "Yb": 173.04000,
            "Lu": 174.96700, "Hf": 178.49000, "Ta": 180.94790, "W": 183.84000, "Re": 186.20700,
            "Os": 190.23000, "Ir": 192.21700, "Pt": 195.07800, "Au": 196.96655, "Hg": 200.59000,
            "Tl": 204.38330, "Pb": 207.20000, "Bi": 208.98038, "Po": 209.00000, "At": 210.00000,
            "Rn": 222.00000, "Fr": 223.00000, "Ra": 226.00000, "Ac": 227.00000, "Th": 232.03810,
            "Pa": 231.03588, "U": 238.02891, "Np": 237.00000, "Pu": 244.00000, "Am": 243.00000,
            "Cm": 247.00000, "Bk": 247.00000, "Cf": 251.00000, "Es": 252.00000, "Fm": 257.00000,
            "Md": 258.00000, "No": 259.00000, "Lr": 262.00000, "Rf": 261.00000, "Db": 262.00000,
            "Sg": 266.00000, "Bh": 264.00000, "Hs": 277.00000, "Mt": 268.00000, "Ds": 281.00000,
            "Rg": 272.00000, "Cn": 285.00000, "Uuq": 289.00000, "Uuh": 292.00000}

    atoms = []

    # set the required columns for template
    temp_need = ["Element symbol", "X orthogonal Å coordinate", "Y orthogonal Å coordinate",
                 "Z orthogonal Å coordinate"]
    # generate the template for further calculations
    template_temp = RaminCalc.get_template_pdb(temp_need)

    # iterate over each atom
    for l in atom_lines:
        d_temp = RaminCalc.get_custom_data_pdb(l, template_temp)
        temp_atom = {"name":d_temp["Element symbol"],"mass":mass[d_temp["Element symbol"]],"x":float(d_temp["X orthogonal Å coordinate"]),"y":float(d_temp["Y orthogonal Å coordinate"]),"z":float(d_temp["Z orthogonal Å coordinate"])}
        atoms.append(temp_atom)

    # calculate the center of mass in three x,y,z
    center_of_mass = {"x":sum([x["x"]*x["mass"] for x in atoms])/sum([x["mass"] for x in atoms])
                      ,"y":sum([x["y"]*x["mass"] for x in atoms])/sum([x["mass"] for x in atoms])
                      ,"z":sum([x["z"]*x["mass"] for x in atoms])/sum([x["mass"] for x in atoms])}
    # calculate the total mass of atoms
    total_mass = sum([x["mass"] for x in atoms])

    # to calculate radius of gyration we need to follow the formula
    # the formula in format of [latex] =: R_\mathrm{gyr}^2 = \frac{1}{M}\sum_{i=1}^{N} m_i(\mathbf{r}_i - \mathbf{R})^2
    for t in atoms:
        atome_mass = t["mass"]
        radius_of_gyration+=atome_mass*((t["x"]-center_of_mass["x"])**2+(t["y"]-center_of_mass["y"])**2+(t["z"]-center_of_mass["z"])**2)
    # the division for 1/M
    radius_of_gyration /= total_mass
    # final sqrt
    radius_of_gyration = math.sqrt(radius_of_gyration)

    return radius_of_gyration


# Nothing to do here
def print_function(pdb_file):
    atom_lines = pdb_file_reader(pdb_file)

    amino_acid_composition = amino_acid_composition_calculator(atom_lines)
    amino_acid_composition_percentage = amino_acid_composition_percentage_calculator(atom_lines)

    amino_acid_hydrophobicity_composition = amino_acid_hydrophobicity_composition_calculator(amino_acid_composition,
                                                                                             Kyte_Doolittle_scale)
    amino_acid_hydrophobicity_composition_percentage = amino_acid_hydrophobicity_composition_percentage_calculator(
        amino_acid_composition, Kyte_Doolittle_scale)

    atomic_composition = atomic_composition_calculator(atom_lines)
    atomic_composition_percentage = atomic_composition_percentage_calculator(atom_lines)

    amino_acid_charge_compostion = amino_acid_charge_composition_calculator(amino_acid_composition)

    hetero_atom_composition = hetero_atom_residue_counter(hetero_atom_pdb_reader(pdb_file))

    most_distant_residues = most_distant_residue_finder(atom_lines)

    radius_of_gyration = radius_of_gyration_calculator(atom_lines)

    print(f"Amino acid composition:")
    for amino_acid in amino_acid_composition.keys():
        print(
            f"{str(amino_acid)} {str(amino_acid_composition[amino_acid])} {amino_acid_composition_percentage[amino_acid]:.2f}%")

    print(f"\nAmino acids composition categorized on the basis of hydrophobicity:")
    for hydrophobicity in amino_acid_hydrophobicity_composition.keys():
        print(
            f"{str(hydrophobicity)} {str(amino_acid_hydrophobicity_composition[hydrophobicity])} {amino_acid_hydrophobicity_composition_percentage[hydrophobicity]:.2f}%")

    print(f"\nAtomic composition:")
    for atom in atomic_composition.keys():
        print(f"{atom} {atomic_composition[atom]} {atomic_composition_percentage[atom]:.2f}%")

    print("\nCharge composition of protein:")
    print(f"Positively Charged Residues: {str(amino_acid_charge_compostion['Positive'])}")
    print(f"Negatively Charged Residues: {str(amino_acid_charge_compostion['Negative'])}")

    print(f"\nNumber of heteroatoms: {len(hetero_atom_composition.keys())}")
    for heteroatom in hetero_atom_composition.keys():
        print(f"{heteroatom} : {hetero_atom_composition[heteroatom]}")

    print(
        f"\nDistance between most distant residues {most_distant_residues[0][0]} and {most_distant_residues[0][1]} is {most_distant_residues[1]:.2f} Angstrom")

    print(f"\nRadius of gyration: {radius_of_gyration:.2f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdb_parser.py <path_to_pdb_file>")
        print("Example: python pdb_parser.py 1FCN.pdb")
        sys.exit(1)
    print_function(sys.argv[1])
