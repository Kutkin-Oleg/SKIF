ring_kwargs = {
    'eE': 3.0,              # electron energy [GeV]
    'eEspread': 0.00135,    # electron energy spread, relative to eE, [root-mean-square]
    'eI': 0.4,              # ring current, [A]
    'betaX': 15.66,         # Betatron function X [m]
    'betaZ': 2.29,          # Betatron function Z [m]
    'eEpsilonX': 9.586e-2,  # Electron beam emittance X [nm * rad]
    'eEpsilonZ': 9.586e-3,  # Electron beam emittance Z [nm * rad]
}


wiggler_1_5_kwargs = {
    'K': 20.1685,  # deflection parameter
    'period': 48.,  # period length [mm]
    'n': 18,  # number of periods
}

wiggler_nstu_scw_kwargs = {
        'K': 20.2,  # defletion parameter
        'period': 48.,  # period length [mm]
        'n': 40,  # number of periods
}