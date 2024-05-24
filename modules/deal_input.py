# deal with input files & check error (except deal_input.py)
from . import utilities

import os
import glob
import argparse
import json
import pandas as pd
import datetime
from rdkit import Chem
from padelpy import padeldescriptor
#import pybel
from openbabel import pybel

__all__ = [
    "check_convert_smiles",
    "calc_fingerprint_trial",
    "check_proper_smiles",
    "deal",
]


class MyError(Exception):
    pass


def check_convert_smiles(smiles: list) -> list:  # change to single smiles
    smiles_out = []
    for smi in smiles:
        if Chem.MolFromSmiles(smi) is None:
            opb_smi = pybel.readstring("smi", smi).write("smi")
            smiles_out.append(opb_smi)
        else:
            smiles_out.append(smi)
    return smiles_out


def calc_fingerprint_trial(carrer: utilities.DataCarrer, smiles: list) -> pd.DataFrame:
    """
    KlekotaRoth FPだけ計算して、Nanが出ないかを調べる。
    """
    with open(carrer["tmpdir"] + "/" + "molecule_smiles.smi", "w") as o:
        print(*smiles, sep="\n", file=o)
    xml_files = glob.glob("fingerprints_xml/*.xml")
    xml_files.sort()
    fp_list = [
        "AtomPairs2DCount",
        "AtomPairs2D",
        "EState",
        "CDKextended",
        "CDK",
        "CDKgraphonly",
        "KlekotaRothCount",
        "KlekotaRoth",
        "MACCS",
        "PubChem",
        "SubstructureCount",
        "Substructure",
    ]
    fp_dict = dict(zip(fp_list, xml_files))
    padeldescriptor(
        mol_dir=carrer["tmpdir"] + "/" + "molecule_smiles.smi",
        d_file=carrer["tmpdir"] + "/" + "Fingerprints_trial.csv",
        descriptortypes=fp_dict["KlekotaRoth"],
        detectaromaticity=True,
        standardizenitro=True,
        standardizetautomers=True,
        threads=2,
        removesalt=True,
        log=False,
        fingerprints=True,
    )
    # load result  csv
    descs_df = pd.read_csv(
        carrer["tmpdir"] + "/" + "Fingerprints_trial.csv", index_col=0
    )
    return descs_df


def check_proper_smiles(carrer: utilities.DataCarrer) -> utilities.DataCarrer:
    smis_conved = check_convert_smiles(carrer["smiles"])
    if len(smis_conved) != len(carrer["smiles"]):
        raise MyError("error in smiles conversion by Pybel")
    descs_df = calc_fingerprint_trial(carrer, smis_conved)
    if bool(descs_df.isnull().values.sum()):  # Nanの数をカウント
        raise MyError("smiles cannot be converted to fingerprints")
    carrer.record_converted_smiles(smis_conved)
    return carrer


def deal(carrer: utilities.DataCarrer) -> utilities.DataCarrer:
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    parser.add_argument("config")
    args = parser.parse_args()
    # command data hoge/data.csv config hoge/config.pyみたいな使い方想定

    # load config.json
    with open(args.config) as f:
        config = json.load(f)

    # load data as DataFrame
    data = pd.read_csv(args.data)

    # make output directory
    nowtime_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    tmp_dir = "tmp/" + nowtime_str
    os.makedirs(tmp_dir)

    # check data content
    try:
        if len(data[config["name"]]) != len(data[config["smiles"]]):
            raise MyError("number of compound name and compound smiles are different")
    except KeyError:
        raise MyError(
            f'The config file doesnt have correct row name {config["name"]} or {config["smiles"]}'
        )

    # store data in carrer object
    carrer.record_input(data, config, tmp_dir)
    # check proper smiles data[config["smiles"]]
    carrer = check_proper_smiles(carrer)

    return carrer
