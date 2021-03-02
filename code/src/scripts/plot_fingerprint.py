# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This is a script that I wrote for my master thesis
# It loads the coordinates of the aligned fragments. It then divides the
# surrounding space into a number of bins, depending on which resolution is
# set. It counts how many of the contact atoms/ centers of contact groups are
# are in each bin and normalizes that by the total amount of contact atoms or
# groups.
#
# Author: Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import time

import pandas as pd

from classes.Settings import Settings
from classes.Radii import Radii
from classes.Fingerprint import Fingerprint

from helpers.geometry_helpers import (make_coordinate_df)
from helpers.geometry_helpers import distances_closest_vdw_central

from constants.paths import WORKDIR, RADII_CSV, FINGERPRINT_CSV


def main():

    if len(sys.argv) != 3:
        print("Usage: python plot_fingerprint.py <path/to/inputfile> <atom or center to count contact group>")
        sys.exit(1)

    t0 = time.time()

    settings = Settings(WORKDIR, sys.argv[1])
    settings.set_atom_to_count(sys.argv[2])

    try:
        df = pd.read_csv(settings.get_aligned_csv_filename(), header=0)
        avg_frag = pd.read_csv(settings.outputfile_prefix + "_avg_fragment.csv", header=0)
    except FileNotFoundError:
        print('First align and calculate average fragment.')
        sys.exit(2)

    # grab only the atoms that are in the contact groups
    df_central = df[df['label'] == '-']

    radii = Radii(RADII_CSV)
    fingerprint = Fingerprint(FINGERPRINT_CSV, settings)

    coordinate_df = make_coordinate_df(df_central, settings, avg_frag, radii)
    coordinate_df['moved'] = coordinate_df['distance'] - coordinate_df['vdw_closest_atom'] - coordinate_df['longest_vdw']

    fingerprint.make_plot(coordinate_df)
    fingerprint.next()

    while fingerprint.not_done():
        avg_frag_f = avg_frag[avg_frag.label.isin(fingerprint.get_label_list())]
        labels = fingerprint.get_labels()

        coordinate_df_f = distances_closest_vdw_central(coordinate_df, avg_frag_f, labels)

        coordinate_df_f['moved'] = coordinate_df_f['distance' + labels] - coordinate_df_f['vdw_closest_atom' + labels] - coordinate_df_f['longest_vdw']

        fingerprint.make_plot(coordinate_df_f)

        fingerprint.next()

    t1 = time.time() - t0
    print("Duration: %.2f s." % t1)


if __name__ == "__main__":
    main()