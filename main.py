# main.py

import os
import numpy as np
import pandas as pd
import warnings

from modules import utilities
from modules import (
    deal_input,
    preprocess,
    model_prediction,
    interpret_stats,
    output_result,
)


"""
input : data.csv & config.json
config file :
    { "name":"hoge", "smiles":"huga" }
steps :
    deal_input
    error_check
    preprocess
    model_prediction
    interpret_stats
    output_result
"""


def main():
    os.chdir(os.path.dirname(__file__))
    warnings.simplefilter("ignore")
    # tmp dir
    direc = "tmp"
    if not os.path.exists(direc):
        os.makedirs(direc)
    # initialize data carrer
    carrer = utilities.DataCarrer()

    # deal with input files & check error
    carrer = deal_input.deal(carrer)

    # preprocessing
    carrer = preprocess.process(carrer)

    # model prediction
    carrer = model_prediction.make_prediction(carrer)

    # interpret prediction & calc statistics
    # carrer = interpret_stats.deal(carrer)

    output_result.output(carrer)
    return None


if __name__ == "__main__":
    main()
