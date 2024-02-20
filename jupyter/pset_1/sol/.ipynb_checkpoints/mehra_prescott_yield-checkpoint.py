from ... import econutil
from ...econutil import *
from ...econutil.plot import tolColor, GenerateTSPlot
import numpy as np


def solve_Mehra_Prescott(model):

    S = model["SDF"]
    P = model["P"]
    GAMMAG = model["GAMMAG"]

    N = P.shape[0]
    I = np.asmatrix(np.identity(N))
    one = np.asmatrix(np.ones([N, 1]))

    eigval, eigvec = np.linalg.eig(P.transpose())
    idx = np.abs(eigval).argsort()
    eigval = eigval[idx]
    eigvec = eigvec[:, idx]
    PII = eigvec[:, -1] / sum(eigvec[:, -1])

    Rf = 1 / (np.multiply(P, S) * one)
    ERf = Rf.transpose() * PII

    M = np.multiply(np.multiply(P, S), GAMMAG)
    eigval, eigvec = np.linalg.eig(M)
    maxeig = max(eigval)

    if maxeig < 1:
        q = np.linalg.inv(I - M) * (M * one)
        R = np.multiply(
            np.multiply(np.tile(q.transpose(), [N, 1]) + 1, 1 / np.tile(q, [1, N])),
            GAMMAG,
        )
        EtR = np.asmatrix(np.diag(R * P.transpose())).transpose()
        ER = EtR.transpose() * PII
        Re = R - np.tile(Rf, [1, N])
        EtRe = EtR - Rf
        ERe = ER - ERf
    else:
        q = np.asmatrix(np.empty([N, 1])) * np.nan
        R = np.asmatrix(np.empty([N, N])) * np.nan
        EtR = np.asmatrix(np.empty([N, 1])) * np.nan
        ER = np.nan
        Re = np.asmatrix(np.empty([N, N])) * np.nan
        EtRe = np.asmatrix(np.empty([N, 1])) * np.nan
        ERe = np.nan

    capT = 100
    y = np.asmatrix(np.zeros([N, capT]))
    q = np.asmatrix(np.ones([N, 1]))
    for T in range(capT):
        q = np.multiply(P, S) * q
        y[:, T] = -1 / (T + 1) * np.log(q)

    sol = {
        "PII": PII,
        "Rf": Rf,
        "ERf": ERf,
        "q": q,
        "R": R,
        "EtR": EtR,
        "ER": ER,
        "Re": Re,
        "EtRe": EtRe,
        "ERe": ERe,
        "y": y,
    }
    return sol


model = {"PHI": 0.43, "MU": 0.018, "DELTA": 0.036}

model["P"] = np.asmatrix(
    [[model["PHI"], 1 - model["PHI"]], [1 - model["PHI"], model["PHI"]]]
)
model["GAMMAC"] = np.asmatrix([
    [1 + model["MU"] + model["DELTA"], 1 + model["MU"] - model["DELTA"]],
    [1 + model["MU"] + model["DELTA"], 1 + model["MU"] - model["DELTA"]],
])
model["GAMMAG"] = model["GAMMAC"].copy()

model_vec = [[0.99, 2], [0.96, 2], [0.99, 4]]
yield_curves = [0] * 3

for i, m in enumerate(model_vec):
    model["BETA"] = m[0]
    model["GAMMA"] = m[1]
    model["SDF"] = model["BETA"] * np.power(model["GAMMAC"], -model["GAMMA"])
    sol = solve_Mehra_Prescott(model)
    yield_curves[i] = sol["y"]

capT = yield_curves[0].shape[1]

param = {
    "figsize": [15, 6],
    "fontsize": 16,
    "subplots": [1, 2],
    "title": "",
    "xlim": [0, capT],
    "ylim": [0, 9],
    "xlabel": "maturity $T$",
    "ylabel": "yield $y^{[T]}_1$",
    "ylogscale": False,
    "showgrid": True,
    "highlightzero": False,
    "showNBERrecessions": False,
    "showNBERrecessions_y": [0, 7],
}

fig, ax = GenerateTSPlot(param)

ax[0, 0].plot(
    np.linspace(1, capT, capT),
    np.squeeze(np.asarray(yield_curves[0][0, :])) * 100,
    linewidth=1,
    marker="*",
    color=tolColor["tolVibrantBlue"],
    linestyle="solid",
    label="$\\beta = "
    + str(model_vec[0][0])
    + "$, $\\gamma = "
    + str(model_vec[0][1])
    + " $",
)
ax[0, 0].plot(
    np.linspace(1, capT, capT),
    np.squeeze(np.asarray(yield_curves[1][0, :])) * 100,
    linewidth=1,
    marker="*",
    color=tolColor["tolVibrantOrange"],
    linestyle="solid",
    label="$\\beta = "
    + str(model_vec[1][0])
    + "$, $\\gamma = "
    + str(model_vec[1][1])
    + " $",
)
ax[0, 0].plot(
    np.linspace(1, capT, capT),
    np.squeeze(np.asarray(yield_curves[2][0, :])) * 100,
    linewidth=1,
    marker="*",
    color=tolColor["tolVibrantTeal"],
    linestyle="solid",
    label="$\\beta = "
    + str(model_vec[2][0])
    + "$, $\\gamma = "
    + str(model_vec[2][1])
    + " $",
)

ax[0, 0].set_title("Yield curve for state $e_1$")
x = ax[0, 0].legend(loc="lower right")

ax[0, 1].plot(
    np.linspace(1, capT, capT),
    np.squeeze(np.asarray(yield_curves[0][1, :])) * 100,
    linewidth=1,
    marker="*",
    color=tolColor["tolVibrantBlue"],
    linestyle="solid",
    label="$\\beta = "
    + str(model_vec[0][0])
    + "$, $\\gamma = "
    + str(model_vec[0][1])
    + " $",
)
ax[0, 1].plot(
    np.linspace(1, capT, capT),
    np.squeeze(np.asarray(yield_curves[1][1, :])) * 100,
    linewidth=1,
    marker="*",
    color=tolColor["tolVibrantOrange"],
    linestyle="solid",
    label="$\\beta = "
    + str(model_vec[1][0])
    + "$, $\\gamma = "
    + str(model_vec[1][1])
    + " $",
)
ax[0, 1].plot(
    np.linspace(1, capT, capT),
    np.squeeze(np.asarray(yield_curves[2][1, :])) * 100,
    linewidth=1,
    marker="*",
    color=tolColor["tolVibrantTeal"],
    linestyle="solid",
    label="$\\beta = "
    + str(model_vec[2][0])
    + "$, $\\gamma = "
    + str(model_vec[2][1])
    + " $",
)

ax[0, 1].set_title("Yield curve for state $e_2$")
ax[0, 1].set_ylabel("yield $y^{[T]}_2$")
x = ax[0, 1].legend(loc="lower right")

fig.set_facecolor("#FFFFFF")
fig.savefig("graphs/asset_pricing_mehra_prescott_yield_curves.pdf", bbox_inches="tight")
