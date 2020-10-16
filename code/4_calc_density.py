# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This is a script that I wrote for my master thesis
# It loads the coordinates of the aligned fragments. It then divides the 
# surrounding space into a number of bins, depending on which resolution is 
# set. It counts how many of the contact atoms/ centers of contact groups are
# are in each bin and normalizes that by the total amount of contact atoms or 
# groups. Then a plot is made that shows the density of the contacts in "4D". 
#
# Author: Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
import math
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

from classes.Settings import Settings
from helpers.density_helpers import prepare_df
from helpers.geometry_helpers import (make_coordinate_df,
                                      calculate_longest_vdw_radius_contact,
                                      make_avg_fragment_if_not_exists)
from helpers.helpers import read_results_alignment


def main():

    if len(sys.argv) != 4:
        print("Usage: python plot_density.py <path/to/inputfile> <resolution> <atom or center to count>")
        sys.exit(1)
    
    settings = Settings(sys.argv[1])
    settings.set_atom_to_count(sys.argv[3])

    # resolution of the bins, in Angstrom
    settings.set_resolution(float(sys.argv[2]))

    df = read_results_alignment(settings.get_aligned_csv_filename())
    avg_fragment = make_avg_fragment_if_not_exists(settings, df)

    # grab only the atoms that are in the contact groups
    df = df[df.in_central_group == False]
    coordinate_df = make_coordinate_df(df, settings, avg_fragment)
  
    try:
        density_df = pd.read_hdf(settings.get_density_df_filename(), settings.get_density_df_key())
    except (FileNotFoundError, KeyError):
        empty_density_df = prepare_df(fragments_df=coordinate_df, settings=settings)

        print("Bins: ", len(empty_density_df), '\nPoints:', len(coordinate_df))

        density_df = count_points_per_square(df=empty_density_df, contact_points_df=coordinate_df, settings=settings)

        # save so we can use the data but only change the plot - saves time :)
        density_df.to_hdf(settings.get_density_df_filename(), settings.get_density_df_key())


def count_points_per_square(df, contact_points_df, settings):
    contact_points_df = contact_points_df

    print("Counting points per bin: ")
    # prepare vector that will contain the amount
    amount = np.zeros(len(df))

    bin_coordinates = np.array([df.xstart, df.ystart, df.zstart])
    contact_coordinates = np.transpose(np.array([contact_points_df.atom_x, contact_points_df.atom_y, contact_points_df.atom_z]))

    amount = fill_bins(amount, bin_coordinates, contact_coordinates, settings.resolution)

    df[settings.to_count_contact] = amount

    return df


def fill_bins(amount, bin_coordinates, contact_coordinates, resolution):
    x, y, z = 0, 1, 2
    for cor in tqdm(contact_coordinates):
        idx = np.where((bin_coordinates[x] <= cor[x]) & (bin_coordinates[x] + resolution >= cor[x]) &
                        (bin_coordinates[y] <= cor[y]) & (bin_coordinates[y] + resolution >= cor[y]) &
                        (bin_coordinates[z] <= cor[z]) & (bin_coordinates[z] + resolution >= cor[z]))
        
        amount[idx] += 1

    return amount


if __name__ == "__main__":
    main()