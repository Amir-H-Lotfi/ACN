from typing import List, Dict

import pathlib
import numpy as np

import utilities as ut
import constants


import matplotlib.pyplot as plt
import matplotlib.figure as figure

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATHS = {
    "root": ROOT,
    "rdata": ROOT.parent.joinpath("data").joinpath("raw"),
    "pdata": ROOT.parent.joinpath("data").joinpath("processed"),
    "plot": ROOT.parent.joinpath("reports").joinpath("py.plots"),
    "style": ROOT.joinpath("matplotlib.config").joinpath("scientific.mplstyle"),
}

plt.style.use(PATHS["style"])


def load_data(src: pathlib.Path) -> Dict:
    data = np.loadtxt(src, delimiter=",", skiprows=1, dtype=np.float64)
    wn, kna, _ = data.T
    fhz, fthz, sl, al = list(), list(), list(), list()

    DISTANCE_CM: np.float64 = np.float64(10)
    DISTANCE_M: np.float64 = np.float64(0.1)

    for _wn, _kna in zip(wn, kna):
        _fhz = _wn * 100 / constants.LIGHT_SPEED
        _fthz = (_wn * 100 / constants.LIGHT_SPEED) / constants.TERA
        _sl = ut.spreading_loss(_fhz, DISTANCE_M)
        _al = ut.absorption_loss(_kna, DISTANCE_CM)
        fhz.append(_fhz)
        fthz.append(_fthz)
        sl.append(_sl)
        al.append(_al)

    fhz = np.array(fhz, dtype=np.float64)
    fthz = np.array(fthz, dtype=np.float64)
    sl = np.array(sl, dtype=np.float64)
    al = np.array(al, dtype=np.float64)

    return {"wn": wn, "kna": kna, "fhz": fhz, "fthz": fthz, "sl": sl, "al": al}


def plot(data: Dict) -> List[figure.Figure]:
    wn, kna = data["wn"], data["kna"]
    fthz = data["fthz"]
    sl, al = data["sl"], data["al"]

    # first plot of kna vs wn
    fig1, ax1 = plt.subplots()
    kna_mean = kna.mean()
    ax1.plot(wn, kna, linestyle="-")
    ax1.set_xlabel(r"Wavenumber $(\mathrm{cm}^{-1})$")
    ax1.set_ylabel(r"Absorption Coefficient $K_{}(f)\;(\mathrm{cm}^{-1})$")
    ax1.set_title("Absorption Coefficient vs Wavenumber")
    ax1.text(
        0.02,
        0.95,
        f"Absorption coefficient mean = {kna_mean:.3e} cm$^{{-1}}$",
        transform=ax1.transAxes,
        verticalalignment="top",
    )

    # second plot of kna vs frequency
    fig2, ax2 = plt.subplots()
    kna_mean = kna.mean()
    ax2.plot(fthz, kna, linestyle="-")
    ax2.set_xlabel("Frequency (THz)")
    ax2.set_ylabel("Absorption Coefficient $K_{}(f)\;(\mathrm{cm}^{-1})$")
    ax2.set_title("Absorption Coefficient vs Frequency")
    ax2.text(
        0.02,
        0.95,
        f"Absorption coefficient mean = {kna_mean:.3e} cm$^{{-1}}$",
        transform=ax2.transAxes,
        verticalalignment="top",
    )

    # third plot of spreading loss vs frequency
    fig3, ax3 = plt.subplots()
    sl_mean = sl.mean()
    ax3.plot(fthz, sl, linestyle="-")
    ax3.set_xlabel("Frequency (THz)")
    ax3.set_ylabel("Spreading Loss (dB)")
    ax3.set_title("Spreading Loss vs Frequency")
    ax3.text(
        0.02,
        0.95,
        f"Spreading Loss mean ={sl_mean:.3e} dB",
        transform=ax3.transAxes,
        verticalalignment="top",
    )

    # forth plot of absoption loss vs frequency
    al_mean = al.mean()
    fig4, ax4 = plt.subplots()
    ax4.plot(fthz, al, linestyle="-")
    ax4.set_xlabel("Frequency (THz)")
    ax4.set_ylabel("Absorption Loss (dB)")
    ax4.set_title("Absorption Loss vs Frequency")
    ax4.text(
        0.02,
        0.95,
        f"Absorption Loss mean = {al_mean:.3}",
        transform=ax4.transAxes,
        verticalalignment="top",
    )

    return [
        fig1,
        fig2,
        fig3,
        fig4,
    ]


def save(
    figs: List[figure.Figure],
    basename: str,
    output: pathlib.Path,
) -> None:
    afig, bfig, cfig, dfig = figs[0], figs[1], figs[2], figs[3]

    ofdir = output.joinpath(basename + "_plots")
    ofdir.mkdir(exist_ok=True)

    ofname1 = ofdir.joinpath(basename + ".0_kna.wn.png")
    afig.savefig(ofname1)
    plt.close(afig)

    ofname2 = ofdir.joinpath(basename + ".1_kna.freq.png")
    bfig.savefig(ofname2)
    plt.close(bfig)

    ofname3 = ofdir.joinpath(basename + ".2_sl.freq.png")
    cfig.savefig(ofname3)
    plt.close(cfig)

    ofname4 = ofdir.joinpath(basename + ".3_al.freq.png")
    dfig.savefig(ofname4)
    plt.close(dfig)


def main():
    for rfile in PATHS["rdata"].iterdir():
        if rfile.exists() and rfile.is_file():
            ut.to_csv(rfile, PATHS["pdata"])

    for pfile in PATHS["pdata"].iterdir():
        if pfile.exists() and pfile.is_file():
            data = load_data(pfile)
            figures = plot(data)
            save(figures, pfile.stem, PATHS["plot"])



main()
