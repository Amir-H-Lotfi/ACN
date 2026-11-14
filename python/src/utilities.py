import pathlib
import numpy as np

import constants


def spreading_loss(frequency: np.float64, distance: np.float64) -> np.float64:
    return 20 * np.log10((4 * np.pi * frequency * distance) / constants.LIGHT_SPEED)


def absorption_loss(
    absorption_coefficient: np.float64, distance: np.float64
) -> np.float64:
    return np.exp(absorption_coefficient * distance)


def to_csv(src: pathlib.Path, dst: pathlib.Path) -> None:
    if src.exists() and src.is_file():
        data = np.loadtxt(src, comments="#", dtype=np.float64)
        ofile = dst.joinpath(src.stem + "_touch.csv")
        ofile.touch()
        np.savetxt(
            ofile,
            data,
            delimiter=",",
            header="WN,KNa,Ka",
            comments="",
            fmt="%.17g",
            encoding="utf-8",
        )
