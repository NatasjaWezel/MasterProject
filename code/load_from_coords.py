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
from classes.Settings import Settings

import csv
import sys

from progressbar import ProgressBar

from tqdm import tqdm

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python load_from_coords.py <path/to/inputfile> <atom to put on origin>")
        sys.exit(1)
    
    filename = sys.argv[1]
    central_group = sys.argv[2]
    
    settings = Settings(filename)
    settings.set_central_group(central_group)

    outputfile = open(settings.outputfilename, 'a', newline='')
    writer = csv.writer(outputfile)

    coordinate_lines = read_coord_file(filename=filename)
    fragments = load_fragments_from_coords(coordinate_lines)

    print("Aligning fragments and writing result to csv")
    for fragment in tqdm(fragments):
        fragment.define_central_group(settings)  
              
        #     fragment.center_coordinates()

        #     atoms_to_put_in_plane = fragment.find_atoms_for_plane()

        #     fragment = perform_rotations(fragment, atoms_to_put_in_plane)
            
        #     fragment.invert_if_neccessary()

        #     write_fragment_to_csv(writer, fragment)
    
    # outputfile.close()
                

def write_fragment_to_csv(writer, fragment):
    """ This function saves the information of the fragment to a CSV file. """
    
    # [print(atom) for atom in fragment.atoms.values()]

    [writer.writerow([fragment.id, fragment.from_entry, atom.label, atom.symbol, atom.part_of, atom.x, atom.y, atom.z]) for atom in fragment.atoms.values()]

def read_coord_file(filename):
    """ Reads the file and saves its lines as a list. """

    with open(filename) as inputfile:
        lines = inputfile.readlines()

    return lines

def load_fragments_from_coords(lines):
    """ Reads part of the coordinate file and returns an entire fragment. """

    fragments = []
    fragment = None
    
    print("Reading fragments from .cor file")
    for line in tqdm(lines):
        
        if "FRAG" in line and fragment == None:
            information = line.split("**")
            fragment = Fragment(fragment_id=information[2].strip(), from_entry=information[0].strip())
            
        elif "FRAG" in line:
            fragments.append(fragment)

            # if we found the header of the next fragment, return
            information = line.split("**")
            fragment = Fragment(fragment_id=information[2].strip(), from_entry=information[0].strip())

        else:
            information = line.split()
            x, y, z = information[1].split("("), information[2].split("("), information[3].split("(")

            atom = Atom(label=information[0].strip("%"), coordinates=[float(x[0]), float(y[0]), float(z[0])])

            atom = check_if_label_exists(atom, fragment)

            fragment.add_atom(atom)

    fragments.append(fragment)

    # this return is here for the last fragment                   
    return fragments
    

if __name__ == "__main__":
    main()



