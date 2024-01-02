from typing import Dict, Union, List
from .heatflow import HeatFlow
import matplotlib.pyplot as plt
import numpy as np

from .lib import linearization


def friedman_show(heating_rate: Dict[int, HeatFlow]) -> None:
    font = 14

    for ht in heating_rate:
        heating_rate[ht].range(350, heating_rate[ht].Temp[-1])
        heating_rate[ht].correct_baseline()
        plt.plot(heating_rate[ht].Temp, heating_rate[ht].DSC, label=f"{ht} $K/min$")
    plt.xlabel("$T~[K]$", fontsize=font)
    plt.ylabel("$Heatflow~[mW/mg]$", fontsize=font)
    plt.legend(fontsize=font - 1)
    plt.savefig("Heatflow.jpg", dpi=300)
    plt.close()

    for ht in heating_rate:
        plt.plot(
            heating_rate[ht].Temp, heating_rate[ht].conversion, label=f"{ht} $K/min$"
        )
    plt.xlabel("$T~[K]$", fontsize=font)
    plt.ylabel(r"Conversion $\alpha$", fontsize=font)
    plt.legend(fontsize=font - 1)
    plt.savefig("Conversion.jpg", dpi=300)
    plt.close()

    alphas = np.linspace(0.05, 0.95, 19)
    regres: Dict[float,List] = dict()
    for alpha in alphas:
        regres[alpha] = []

    for ht in heating_rate:
        f = heating_rate[ht].ln_speed_inv_T()
        for alpha in alphas:
            regres[alpha].append(f(alpha))

    energy: Dict[float,List] = dict()
    for alpha in alphas:
        curve = np.array(regres[alpha]).T
        plt.plot(curve[0], curve[1], "o", label=f"${round(alpha, 2)}$")
        w, b, mse = linearization(curve[0], curve[1])
        energy[alpha] = [-w / 1000 * 8.31, mse]
        plt.plot(curve[0], w * curve[0] + b, "-", color="black")

    plt.xlabel("$1/T~[1/K]$", fontsize=font)
    plt.ylabel(r"$\ln (d \alpha/ dt)~[1/s]$ ", fontsize=font)
    plt.legend(fontsize=font - 5)
    plt.savefig("ReactionRate.jpg", dpi=300)
    plt.close()

    for alpha in energy:
        plt.errorbar(
            alpha,
            energy[alpha][0],
            yerr=np.sqrt(energy[alpha][1]) * abs(energy[alpha][0]),
            fmt="o",
            ecolor="red",
            capsize=7,
        )
    plt.xlabel(r"Conversion $\alpha$", fontsize=font)
    plt.ylabel("$E_a~[kJ/mol]$")
    plt.savefig("Energy.jpg", dpi=300)
    plt.close()
