import matplotlib.pyplot as plt

from .reading import read_file


class HeatFlow:
    def __init__(self, file_name: str) -> None:
        self.data = read_file(file_name)
        self.empty = self.data.size == 0

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

    def plot(self, fig_name: str) -> None:
        plt.plot(self.data[0], self.data[2])
        plt.savefig(f"{fig_name}.jpg", dpi=300)
