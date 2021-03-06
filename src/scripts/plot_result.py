# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This script is part of the quantification pipeline of 3D experimental data of crystal structures that I wrote for my
# thesis in the Master Computational Science, University of Amsterdam, 2021.
#
# `plot_result.py` plots a given amount of aligned fragments.
#
# Author: Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys

import pandas as pd

from helpers.plot_functions import plot_fragments

from constants.colors import COLORS


def main():
    if len(sys.argv) != 3:
        print("Usage: python run.py <inputfilename> <fragments_to_plot>")
        sys.exit(1)

    filename = sys.argv[1]
    title = filename.rsplit('\\')[-1].rsplit('.', 1)[0]
    central = title.split("_")[0]
    contact = title.split("_")[1]

    df = pd.read_csv('../../results/pairs/' + central + '/' + central + "_" + contact + "_vdw.5/"
                     + central + "_" + contact + "_aligned.csv")

    df = df[df.label != '-']

    amount = int(sys.argv[2])

    plot_fragments(df, amount, COLORS)


if __name__ == "__main__":
    main()
