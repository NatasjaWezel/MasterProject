import numpy as np

from helpers.tests import test_rotation1, test_rotation2, test_rotation3

def perform_rotations(fragment, atoms_to_put_in_plane):
    """ Performs three rotations to lie three of the atoms in the xy plane, one of those
        on the x-axis. 
        First rotation: puts first atom on xy-plane if it already was on a plane, 
        and above the x-axis if it wasn't by rotating around the z-axis. 
        Second rotation: puts first atom on x-axis by rotating around y-axis.
        Third rotation: puts second atom in x-y plane by rotating around the x-axis. """

    atoms = [atoms_to_put_in_plane[0], atoms_to_put_in_plane[0], atoms_to_put_in_plane[1]]
    axis = ["z", "y", "x"]

    for i, atom in enumerate(atoms):
        coord_vector = find_coord_vector(ax=axis[i], atom=atom)

        angle = find_angles(ax=axis[i], coord_vector=coord_vector)
        angle = find_rotation_direction(ax=axis[i], atom=atom, angle=angle)

        fragment = calculate_rotation(fragment=fragment, angle=angle, ax=axis[i])

        if i == 0:
            test_rotation1(fragment, atoms_to_put_in_plane)
        elif i == 1:
            test_rotation2(fragment, atoms_to_put_in_plane)
        else:
            test_rotation3(fragment, atoms_to_put_in_plane)

    return fragment


def find_coord_vector(ax, atom):
    # if first atom doesn't lie in any plane, some extra preparation is required
    not_in_any_plane = False
    if not atom.x == 0.0 and not atom.y == 0.0 and not atom.z == 0.0:
        not_in_any_plane = True

    coord_vector = [atom.x, atom.y, atom.z]

    # if the atom is not in a single plane, project it onto the xy plane for the first rotation
    if not_in_any_plane:
        if ax == "x":
            coord_vector = [0, atom.y, atom.z]
        elif ax == "y":
            coord_vector = [atom.x, 0, atom.z]
        else:
            coord_vector = [atom.x, atom.y, 0]

    return coord_vector


def find_rotation_direction(ax, atom, angle):
    """ Defines the direction of the rotation, clockwise or counter clockwise. """ 
    
    if ax == "x" and atom.z < 0:
        angle = -angle
    elif ax == "y" and atom.z < 0:
        angle = -angle
    elif ax == "z" and atom.y < 0:
        angle = -angle

    return angle


def find_angles(coord_vector, ax):
    """ Rotates the molecule so that the contact fragment is always in the same position. 
        Rotates only the important part of the molecule. """

    # x, y, z unitary row vectors:
    x, y =  np.array([1, 0, 0]), np.array([0, 1, 0])

    point_vector = np.array(coord_vector)
    
    # formula: u.v = |u|.|v|.cos(alpha)
    # alpha = arccos((u.v)/(|u|.|v|))
    if ax == "x":
        # return angle with y axis (beta)
        return np.arccos(np.dot(point_vector, y) / np.linalg.norm(point_vector))
    elif ax == "y" or ax == "z":
        # return angle with x axis (alpha)
        return np.arccos(np.dot(point_vector, x) / np.linalg.norm(point_vector))
    else:
        assert ax in ["x", "y", "z"], "Ax must be either x, y or z."


def calculate_rotation(fragment, angle, ax):
    # rotate all coordinates according to the previously defined rotation matrices
    for atom in fragment.atoms.values():
        coord_vector = np.array([atom.x, atom.y, atom.z])

        if ax == "x":
            coord_vector = np.dot(coord_vector, rotate_x(angle))
        elif ax == "y":
            coord_vector = np.dot(coord_vector, rotate_y(angle))
        else:  
            coord_vector = np.dot(coord_vector, rotate_z(angle))
            
        atom.x, atom.y, atom.z = coord_vector[0], coord_vector[1], coord_vector[2]

    return fragment


def rotate_x(angle):
    """ Rotation matrix for rotation around x-axis. """

    return np.array(( [1,             0,              0], 
                        [0,             np.cos(angle),  -np.sin(angle)], 
                        [0,             np.sin(angle),  np.cos(angle)]))


def rotate_y(angle):
    """ Rotation matrix for rotation around y-axis. """

    return np.array(( [np.cos(angle),  0,              -np.sin(angle)], 
                        [0,             1,              0], 
                        [np.sin(angle),  0,              np.cos(angle)]))


def rotate_z(angle):
    """ Rotation matrix for rotation around z-axis. """

    return np.array(( [np.cos(angle), -np.sin(angle), 0], 
                        [np.sin(angle), np.cos(angle),  0], 
                        [0,             0,              1]))