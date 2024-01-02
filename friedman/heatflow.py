import numpy as np
from scipy import interpolate

from .baseline import baseline
from .lib import bigest_negative_interval, integral_transform
from .reading import read_file


class HeatFlow:
    def __init__(self, file_name: str, to_K_sec: bool = True) -> None:
        self.data = read_file(file_name)
        if self.data.size < 3:
            raise ImportError(f"HeatFlow: file {file_name} is not correct")
        if to_K_sec:
            self.data[0] += 273.15
            self.data[1] *= 60

    @property
    def Temp(self):
        return self.data[0]

    @property
    def Time(self):
        return self.data[1]

    @property
    def DSC(self):
        return self.data[2]

    @property
    def conversion(self):
        conv = integral_transform(self.data[2])
        conv[:] /= conv[-1]
        return conv

    def range(self, Tmin: float, Tmax: float) -> None:
        if Tmin > Tmax:
            Tmin, Tmax = Tmax, Tmin
        for i in range(len(self.data[0])):
            if self.data[0, i] > Tmin:
                self.data = self.data[:, i:]
                break
        for i in range(len(self.data[0]) - 1, 0, -1):
            if self.data[0, i] < Tmax:
                self.data = self.data[:, :i]
                break

    def correct_baseline(self, **kwargs) -> None:
        dsc = np.copy(self.data[2])
        dsc -= baseline(dsc, **kwargs)
        a, b = bigest_negative_interval(dsc)
        dsc = np.copy(self.data[2])[a:b]
        dsc -= baseline(dsc, **kwargs)
        self.data[2] = 0.0
        self.data[2, a:b] = dsc

    def ln_speed_inv_T(self):
        alpha = self.conversion
        speed = np.gradient(alpha) / np.gradient(self.Time)
        tepm_from_alpha = interpolate.interp1d(
            alpha, self.Temp, fill_value="extrapolate"
        )
        speed_from_alpha = interpolate.interp1d(alpha, speed, fill_value="extrapolate")
        return lambda x: (1.0 / tepm_from_alpha(x), np.log(speed_from_alpha(x)))
