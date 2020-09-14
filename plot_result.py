from helpers.helpers import plot_fragments

import pickle

from helpers.Fragment import Fragment
from helpers.Atom import Atom
import pandas as pd

import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py <inputfilename>")
        sys.exit(1)
    
    filename = sys.argv[1]


    df = pd.read_csv(filename, header=None)
    df.columns = ["entry_id", "fragment_id", "atom_label", "part_of", "atom_x", "atom_y", "atom_z"]

    fragments = []
    labels = []

    unique_entrys = df.entry_id.unique()
    
    for unique_entry in unique_entrys:
        smalldf = df[df.entry_id == unique_entry]

        fragment_ids = smalldf.fragment_id.unique()
        for fragment_id in fragment_ids:
            atoms = smalldf[smalldf.fragment_id == fragment_id]
            
            fragment = Fragment(unique_entry, fragment_id)

            for _, row in atoms.iterrows():
                atom = Atom(row.atom_label, row.atom_x, row.atom_y, row.atom_z)
                fragment.add_atom(atom)
            
            fragment.set_center('N')
            fragment.find_bonds_NO3_and_distances()
            fragments.append(fragment)
            labels.append(unique_entry + str(fragment_id))

    amount = 10
    
    plot_fragments(fragments[:amount], labels[:amount])


if __name__ == "__main__":
    main()