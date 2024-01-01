import os

import matplotlib.pyplot as plt

from friedman import HeatFlow
import numpy as np

if __name__ == "__main__":
    HF = HeatFlow(os.path.join("data", "PB2_Astr_0.05%_3K.txt"))
    HF.range(77, 205)
    HF.correct_baseline()
    plt.plot(HF.conversion, np.log(np.gradient(HF.conversion) / np.gradient(HF.Time)))
    plt.show()
    # HF.plot("hf")
