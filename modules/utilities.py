# utilities
import pandas as pd
import numpy as np


class DataCarrer:
    def __init__(self) -> None:
        self.fingerprints: pd.DataFrame = pd.DataFrame()

    def record_input(self, data, config, tmp_dir) -> None:
        """
        data : pd.DataFrame
            name : compound name
            smiles : compound smiles
        config : dict
        tmp_dir : str
        """
        self.data: pd.DataFrame = data
        self.config: dict = config
        self.tmpdir_path = tmp_dir

    def record_fingerprints(self, fp: pd.DataFrame):
        """
        fp : fingeprint (type : pd.DataFrame)
        """
        self.fingerprints = fp

    def record_converted_smiles(self, smiles: list):
        self.data[self.config["smiles"]] = smiles

    def record_prediction(self, results: np.ndarray):
        self.data["pIC50"] = results

    def __getitem__(self, key):
        if key == "name":
            return self.data[self.config["name"]].values.tolist()
        elif key == "smiles":
            return self.data[self.config["smiles"]].values.tolist()
        elif key == "predicton":
            return self.data["pIC50"].values.tolist()
        elif key == "config":
            return self.config
        elif key == "fingerprints":
            return self.fingerprints
        elif key == "tmpdir":
            return self.tmpdir_path
        else:
            return self.data
