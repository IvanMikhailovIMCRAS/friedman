import os

from friedman import HeatFlow, friedman_show

if __name__ == "__main__":
    ht = {
        3: HeatFlow(os.path.join("data", "PB2_Astr_0.05%_3K.txt")),
        5: HeatFlow(os.path.join("data", "PB2_Astr_0.05%_5K.txt")),
        10: HeatFlow(os.path.join("data", "PB2_Astr_0.05%_10K.txt")),
        15: HeatFlow(os.path.join("data", "PB2_Astr_0.05%_15K.txt")),
        20: HeatFlow(os.path.join("data", "PB2_Astr_0.05%_20K.txt")),
    }
    model = friedman_show(heating_rate=ht)
