import matplotlib.pyplot as plt

from .baseline import baseline
from .lib import integral_transform
from .reading import read_file


class HeatFlow:
    def __init__(self, file_name: str) -> None:
        self.data = read_file(file_name)
        if self.data.size < 3:
            raise ImportError(f"HeatFlow: file {file_name} is not correct")
        self.data[3, :] = 0.0

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
        self.data[2] -= baseline(self.data[2], **kwargs)

    def plot(self, fig_name: str) -> None:
        plt.plot(self.data[0], self.data[2])
        plt.savefig(f"{fig_name}.jpg", dpi=300)
