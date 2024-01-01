import codecs
import warnings

import numpy as np


def read_file(file_name: str) -> np.ndarray:
    """_summary_

    Args:
        file_name (str): path to the DSC data file (*.txt)

    Returns:
        Optional[np.ndarray]: Temp./C; Time/min; DSC/(mW/mg); Sensit./(uV/mW)
        or empty array if format is uncorrect
    """
    with open(file_name, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    n: int = 0
    for line in lines:
        n += 1
        if "Temp" in line:
            break
        filecp = codecs.open(file_name, encoding="cp1252")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = np.loadtxt(filecp, skiprows=n, delimiter=";")
        data = data.T
    return data
