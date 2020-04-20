import numpy as np
import pandas as pd

CSV_FILES_PATH = "../csv/"
SEASON_START = 2009
SEASON_END = 2019

def read_input(filename, header=0):
    return pd.read_csv(CSV_FILES_PATH + filename + ".csv", sep="|", header=header)


def save_output_to_csv(output, filename):
    output.to_csv(CSV_FILES_PATH + filename + ".csv", sep="|", index=False)

teams = read_input("teams")
cl_qualifiers = read_input("cl_qualifiers")
el_qualifiers = read_input("el_qualifiers")

season_results = read_input("season_results")
