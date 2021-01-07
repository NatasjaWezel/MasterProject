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

import sys

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

from classes.Settings import Settings
from helpers.plot_functions import plot_density, plot_fragment_colored


def main():

    if len(sys.argv) != 4:
        print("Usage: python analyze_density.py <path/to/inputfile> <resolution> <atom or center to count>")
        sys.exit(1)

    settings = Settings(sys.argv[1])

    # resolution of the bins, in Angstrom
    settings.set_resolution(float(sys.argv[2]))

    settings.set_atom_to_count(sys.argv[3])

    try:
        avg_fragment = pd.read_csv(settings.get_avg_frag_filename())
        density_df = pd.read_hdf(settings.get_density_df_filename(), settings.get_density_df_key())
    except (FileNotFoundError, KeyError) as exception:
        print(exception)
        print("Run avg_frag and calc_density first")
        sys.exit(1)

    make_plot(avg_fragment, density_df, settings)


def make_plot(avg_fragment, density_df, settings):
    plotname = settings.get_density_plotname()
    fig = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection='3d')

    ax = plot_fragment_colored(ax, avg_fragment)

    p, ax = plot_density(ax=ax, df=density_df, settings=settings)

    ax.set_title(f"{settings.central_group_name}--{settings.contact_group_name} 4D density plot\n\
                    Resolution: {settings.resolution}")

    fig.colorbar(p)
    plt.savefig(plotname)
    plt.show()


if __name__ == "__main__":
    main()