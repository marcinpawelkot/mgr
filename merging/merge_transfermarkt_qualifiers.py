import numpy as np
import pandas as pd

from helpers.utils import read_input, save_output_to_csv


def run():
    teams_dl_uefa_record = read_input("teams_dl_uefa_record")
    cl_qualifiers = read_input("cl_qualifiers_aggregated")
    el_qualifiers = read_input("el_qualifiers_aggregated")

    teams_dl_uefa_record["TransfermarktId"] = teams_dl_uefa_record["Link"].str.split(expand=True, pat='/')[
        4].astype(int)

    teams_dl_uefa_qualifiers_record = pd.merge(teams_dl_uefa_record,
                                               cl_qualifiers,
                                               how="left",
                                               left_on=["TransfermarktId", "Year"],
                                               right_on=["TransfermarktId", "Year"]).merge(el_qualifiers,
                                                                                           how="left",
                                                                                           left_on=["TransfermarktId",
                                                                                                    "Year"],
                                                                                           right_on=["TransfermarktId",
                                                                                                     "Year"])
    teams_dl_uefa_qualifiers_record.replace(np.nan, 0, inplace=True)

    save_output_to_csv(teams_dl_uefa_qualifiers_record, "teams_dl_uefa_qualifiers_record")
