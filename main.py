from friedman import HeatFlow

if __name__ == "__main__":
    HF = HeatFlow("PB2_Astr_0.05%_3K.txt")
    HF.range(77, 205)
    HF.plot("hf")
