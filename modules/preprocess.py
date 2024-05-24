# preprocessing block
from . import utilities

import pandas as pd
import glob
from padelpy import padeldescriptor

__all__ = [
    "calc_fingerprint",
    "process",
]


class MyError(Exception):
    pass


def calc_fingerprint(
    carrer: utilities.DataCarrer, smiles_path: str, fptype: str
) -> pd.DataFrame:
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
    xml_files = glob.glob("fingerprints_xml/*.xml")
    xml_files.sort()
    fp_dict = dict(zip(fp_list, xml_files))
    # calc fp
    padeldescriptor(
        mol_dir=smiles_path,
        d_file=carrer["tmpdir"] + "/" + f"{fptype}_process.csv",
        descriptortypes=fp_dict[fptype],
        detectaromaticity=True,
        standardizenitro=True,
        standardizetautomers=True,
        threads=4,
        removesalt=True,
        log=False,
        fingerprints=True,
    )
    descs_df = pd.read_csv(
        carrer["tmpdir"] + "/" + f"{fptype}_process.csv", index_col=0
    )
    return descs_df


def process(carrer: utilities.DataCarrer) -> utilities.DataCarrer:
    smi_path = carrer["tmpdir"] + "/" + "molecule_smiles_process.smi"
    fplist = ["MACCS", "PubChem", "KlekotaRoth"]
    fp_df_list = []

    with open(smi_path, "w") as o:
        print(*carrer["smiles"], sep="\n", file=o)

    # calc descriptors
    for fptype in fplist:
        fp_df_list.append(calc_fingerprint(carrer, smi_path, fptype))
    fp_list = pd.concat(fp_df_list, axis=1)

    # select fp which model needs
    with open("./models/descriptors_ML.txt", "r", encoding="utf-8") as f:
        demanded_fp_list = f.read().split("\n")
    fp_df_sele = fp_list.loc[:, demanded_fp_list]

    # descriptorをcarrerへ格納
    carrer.record_fingerprints(fp_df_sele)
    # error check
    if bool(carrer["fingerprints"].isnull().values.sum()):  # Nanの数をカウント
        raise MyError("smiles cannot be converted to fingerprints")
    return carrer
