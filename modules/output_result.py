# output result
from . import utilities

import os
import json
import pandas as pd


def output(carrer: utilities.DataCarrer):
    output_path = "output"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    carrer["data"].to_csv(output_path + "/" + "output.csv", index=False)
    # dump json
    with open(output_path + "/" + "config.json", "w") as f:
        json.dump(carrer["config"], f, indent=2)
    return None
