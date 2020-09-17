import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from helpers.tests import test_count

from helpers.Atom import Atom
from helpers.Fragment import Fragment

def average_molecule(df):
    """ Returns a fragment containing the bonds and average points of the interacting molecule. """ 

    # TODO: make it an actual average
    # TODO: know which O is which O?
    central_group_df = df[df.fragment_or_contact == "c"]

    entry_id = central_group_df.entry_id.unique()[0]
    fragment_id = central_group_df.fragment_id.unique()[0]

    fragment = Fragment(entry_id, fragment_id)

    for _, row in central_group_df[(central_group_df.fragment_id == fragment_id) & (central_group_df.entry_id == entry_id)].iterrows():
        atom = Atom(row.atom_label, row.atom_x, row.atom_y, row.atom_z)
        fragment.add_atom(atom)

    return fragment    


def find_maximum(df):
    """ Returns the largest coordinate for each of the x, y and z axis. """

    maxx = df.atom_x.max()
    maxy = df.atom_y.max()
    maxz = df.atom_z.max()

    return maxx, maxy, maxz

def find_minimum(df):
    """ Returns the smallest coordinate for each of the x, y and z axis. """

    minx = df.atom_x.min()
    miny = df.atom_y.min()
    minz = df.atom_z.min()

    return minx, miny, minz
   
def prepare_df(fragments_df, resolution, to_count):
    maxx, maxy, maxz = find_maximum(fragments_df)
    minx, miny, minz = find_minimum(fragments_df)

    # TODO: check if this is entirely correct
    # i think the volumes still differ per search now
    no_bins_x = math.ceil((maxx + abs(minx))/resolution)
    no_bins_y = math.ceil((maxy + abs(miny))/resolution)
    no_bins_z = math.ceil((maxz + abs(minz))/resolution)

    amount_bins = no_bins_x * no_bins_y * no_bins_z

    print("Bins: ", no_bins_x, no_bins_y, no_bins_z)

    bins = [np.linspace(minx, maxx, num=no_bins_x + 1),
            np.linspace(miny, maxy, num=no_bins_y + 1),
            np.linspace(minz, maxz, num=no_bins_z + 1)] 

    indices = [i for i in range(0, amount_bins)]
    
    df = pd.DataFrame(columns=['xstart', 'xend', 'ystart', 'yend', 'zstart', 'zend'], index=indices)

    current_index = 0
    for i in range(0, no_bins_x):
        xstart, xend = bins[0][i], bins[0][i + 1]

        for j in range(0, no_bins_y):
            ystart, yend = bins[1][j], bins[1][j + 1]

            for k in range(0, no_bins_z):
                zstart, zend = bins[2][k], bins[2][k + 1]
                
                df.loc[current_index] = [xstart, xend, ystart, yend, zstart, zend]
                current_index += 1

    for column in to_count:
        df["amount_" + column] = 0
    
    return df

def plot_density(plotname, to_count, avg_fragment, df, resolution):
    df['ymiddle'] = (df['ystart'] + df['yend']) / 2
    df['xmiddle'] = (df['xstart'] + df['xend']) / 2
    df['zmiddle'] = (df['zstart'] + df['zend']) / 2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot the (average of the) central group 
    for atom in avg_fragment.atoms.values():
        if "O" in atom.label:
            ax.scatter(atom.x, atom.y, atom.z, c="red", s=20, edgecolor="black")
        elif "N" in atom.label:
            ax.scatter(atom.x, atom.y, atom.z, c="blue", s=20, edgecolor="black")

    # for now only use first column
    column = to_count[0]
    columname = "amount_" + column
    # normalize per column 
    df[columname] = df[columname] / df[columname].sum()

    points = df[df[columname] > 0.001]

    norm = plt.Normalize(0.001, points[columname].max())
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightblue","fuchsia","red"])
    
    # TODO: fix sizes of points
    p = ax.scatter(list(points.xmiddle), list(points.ymiddle), list(points.zmiddle), s=list(10000 * points[columname]), c=list(points[columname]), cmap=cmap, norm=norm)

    ax.set_title("4D density plot\n Resolution: " + str(resolution))

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    fig.colorbar(p)
    plt.savefig(plotname)
    plt.show()

def count_points_per_square(df, points_df, to_count):
    
    small_points_df = points_df[points_df.fragment_or_contact == "f"]
    unique_entries = small_points_df.entry_id.unique()
    total_entries = len(unique_entries)

    for i, entry_id in enumerate(unique_entries):
        entry_df = small_points_df[small_points_df.entry_id == entry_id]

        for fragment_id in entry_df.fragment_id.unique():
            fragment_df = entry_df[entry_df.fragment_id == fragment_id]
            
            for column in to_count:
                columname = "amount_" + column
                
                # if center, calculate per fragment instead of per atom
                if "center" == column:
                    # TODO: can it say just C here?
                    x, y, z = calculate_center(fragment_df=fragment_df, atoms=["C"])
                    
                    df = add_one_to_bin(df, columname, x, y, z)
                else:
                    point = fragment_df[fragment_df.atom_label.str.contains(column)]

                    assert (len(point) == 1), " atom label is not unique, can't count per bin"

                    x, y, z = float(point.atom_x), float(point.atom_y), float(point.atom_z)
                    df = add_one_to_bin(df, columname, x, y, z)
        
        if i % 100 == 0:
            print(str(i) + "/" + str(total_entries) + " done")

    # TODO: see if counting is right
    # test_count(df, small_points_df)
    return df

def add_one_to_bin(df, columname, x, y, z):
    # print("In add one to bin function")
    # print(float(x))
    # print(df.columns)
    # print(columname)


    # print(df.xstart)
    # print(x)
    # print(df[df.xstart <= x])


    # print("HOOOOOOOOOOOOOI")


    # TODO: find out what happens with points exactly on a bin-line
    df.loc[(df.xstart <= x) & (df.xend >= x) & 
                (df.ystart <= y) & (df.yend >= y) & 
                (df.zstart <= z) & (df.zend >= z),
                columname] = df[(df.xstart <= x) & (df.xend >= x) & 
                                (df.ystart <= y) & (df.yend >= y) & 
                                (df.zstart <= z) & (df.zend >= z)][columname] + 1

    return df

def calculate_center(fragment_df, atoms):

    # TODO: only count "C" (or other atoms in atoms) for average
    atom_df = fragment_df
    x, y, z = atom_df.atom_x.mean(), atom_df.atom_y.mean(), atom_df.atom_z.mean()

    return x, y, z