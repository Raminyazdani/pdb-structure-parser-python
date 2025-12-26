import sys

"""
PDB Parser for Structural Bioinformatics
"""

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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        atom_lines = pdb_file_reader(sys.argv[1])
        print(f"Read {len(atom_lines)} ATOM lines from {sys.argv[1]}")
