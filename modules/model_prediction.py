# model prediction & shap analysis
from . import utilities

import pandas as pd
import joblib

__all__ = [
    "make_prediction",
]


class MyError(Exception):
    pass


def make_prediction(carrer: utilities.DataCarrer) -> utilities.DataCarrer:
    """
    python, sklearn(たぶんnumpy&pandasも)のバージョンがモデル学習時と同じじゃないとだめらしいので、開発と同じコードで、本番環境（仮想環境）で学習させたモデルを使う。ymlで構築しないといけなさそう。
    """
    # load model
    filename = "models/finalized_model.sav"
    loaded_model = joblib.load(filename)
    # prediction by models
    pred_results = loaded_model.predict(carrer["fingerprints"])  # np.array returned
    
    # Added!!!20240524
    pred_results_add6 = pred_results+6

    # store results in carrer inst
    #carrer.record_prediction(pred_results)
    carrer.record_prediction(pred_results_add6)

    return carrer
