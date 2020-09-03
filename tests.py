from headers import *

def check_new_molecule_alignment(molecule, atom_to_center, atoms_to_put_in_plane):
    
    test_centering(molecule, atom_to_center)
    test_axis_alignment(molecule, atoms_to_put_in_plane)
    test_plane_alignment(molecule, atoms_to_put_in_plane)

    print("Passed all checks, molecule's new alignment is correct.")

def test_centering(molecule, atom_to_center):
    atom = molecule.highlighted_atoms[atom_to_center]
    if atom.x != 0.0 or atom.y != 0.0 or atom.z != 0.0:
        assert atom_to_center + "atom is not centered right"

def test_axis_alignment(molecule, atoms_to_put_in_plane):
    # the first atom is supposed to be on the x axis, so y and z have to be 0
    atom1 = molecule.highlighted_atoms[atoms_to_put_in_plane[0]]
    if atom1.y < -CUT_OFF_ZERO or atom1.y > CUT_OFF_ZERO or atom1.z < -CUT_OFF_ZERO or atom1.z > CUT_OFF_ZERO:
        assert atom1.label + " is not on the x axis, check first and second rotations"

def test_plane_alignment(molecule, atoms_to_put_in_plane):
    # the second atom is supposed to be on the xy plane, so z has to be zero
    atom2 = molecule.highlighted_atoms[atoms_to_put_in_plane[1]]
    if atom2.z < -CUT_OFF_ZERO or atom2.z > CUT_OFF_ZERO:
        assert atom2.label + " is not in the xy plane (check third rotation)"

    