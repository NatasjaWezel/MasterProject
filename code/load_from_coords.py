# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This is a script that I wrote for my master thesis
# It loads the coordinates of the fragments exported from a conquest query and 
# aligns the central groups by using rotation matrices and other linear algebra.
# It then saves the new coordinates in a .csv file.
#
# Author: Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from helpers.rotation_helpers import perform_rotations
from helpers.helpers import check_if_label_exists

from classes.Atom import Atom
from classes.Fragment import Fragment

import csv
import sys

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python load_from_coords.py <path/to/inputfile> <atom to put on origin>")
        sys.exit(1)
    
    filename = sys.argv[1]
    atom_to_center = sys.argv[2]
    
    outputfilename = "results/" + filename.rsplit('\\')[-1].rsplit('.', 1)[0] + "_aligned.csv"

    fragments = load_fragments_from_coords(filename=filename)
    
    rotated_fragments = []

    for fragment in fragments:
        try:
            fragment.set_center(atom_to_center)        
            fragment.center_coordinates()

            atoms_to_put_in_plane = fragment.find_atoms_for_plane()

            fragment = perform_rotations(fragment, atoms_to_put_in_plane)
            
            fragment.invert_if_neccessary()

            rotated_fragments.append(fragment)
        except AssertionError as msg:
            print(msg)
                    
    print(len(rotated_fragments), "/", len(fragments), ' rotated succesfully')

    with open(outputfilename, "a", newline="") as outputfile:
        writer = csv.writer(outputfile)

        for fragment in rotated_fragments:
            for atom in fragment.atoms.values():
                writer.writerow([fragment.from_entry, fragment.fragment_id, fragment.from_entry + fragment.fragment_id, atom.label, atom.symbol, atom.part_of, atom.x, atom.y, atom.z])
    


def load_fragments_from_coords(filename):
    """ Loads a list of fragments from a .cor file. """

    with open(filename) as inputfile:
        lines = inputfile.readlines()

    fragments = []
    fragment = None

    for line in lines:
        if "FRAG" in line:
            if fragment:
                fragments.append(fragment)

            information = line.split('**')
            fragment = Fragment(fragment_id=information[2].strip(), from_entry=information[0].strip())
        else:
            information = line.split()
            x, y, z = information[1].split("("), information[2].split("("), information[3].split("(")

            atom = Atom(label=information[0].strip("%"), coordinates=[float(x[0]), float(y[0]), float(z[0])])

            atom = check_if_label_exists(atom, fragment)

            fragment.add_atom(atom)
            
    fragments.append(fragment)
    
    return fragments

if __name__ == "__main__":
    main()



