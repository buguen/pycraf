#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under GPL v2 - see LICENSE

from __future__ import (
    absolute_import, unicode_literals, division, print_function
    )

import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as apu
from astropy.units.quantity import Quantity
import astropy.constants as con


__all__ = [
    'Aeff_from_Ageom', 'Ageom_from_Aeff',
    'Gain_from_Aeff', 'Aeff_from_Gain',
    'S_from_E', 'E_from_S',
    'Ptx_from_Erx', 'Erx_from_Ptx',
    'S_from_Ptx', 'Ptx_from_S',
    'Prx_from_S', 'S_from_Prx',
    'free_space_loss',
    'Erx_unit', 'R0', 'dB_W', 'dB_mW', 'db_uV_m'
    ]


def Aeff_from_Ageom(Ageom, eta_a):

    assert isinstance(Ageom, apu.Quantity), 'Ageom must be an astropy Quantity object'
    assert isinstance(eta_a, apu.Quantity), 'eta_a must be an astropy Quantity object'

    return Ageom * eta_a


def Ageom_from_Aeff(Aeff, eta_a):

    assert isinstance(Aeff, Quantity), 'Aeff must be an astropy Quantity object'
    assert isinstance(eta_a, Quantity), 'eta_a must be an astropy Quantity object'

    return Aeff / eta_a


def Gain_from_Aeff(Aeff, f):

    assert isinstance(Aeff, Quantity), 'Aeff must be an astropy Quantity object'
    assert isinstance(f, Quantity), 'f must be an astropy Quantity object'

    return 4. * np.pi * Aeff * (f / con.c) ** 2


def Aeff_from_Gain(G, f):

    assert isinstance(G, Quantity), 'G must be an astropy Quantity object'
    assert isinstance(f, Quantity), 'f must be an astropy Quantity object'

    return  G * (con.c / f) ** 2 / 4. / np.pi


def S_from_E(E):
    '''
    Calculate power flux density, S, from field strength.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    E - Received E-field strength

    Returns
    -------
    Power flux density, S
    '''

    assert isinstance(E, Quantity), 'E must be an astropy Quantity object'

    return E ** 2 / R0


def E_from_S(S):
    '''
    Calculate field strength, E, from power flux density.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    S - Power flux density

    Returns
    -------
    Received E-field strength, E
    '''

    assert isinstance(S, Quantity), 'S must be an astropy Quantity object'

    return np.sqrt(S) * R0


def Ptx_from_Erx(Erx, d, Gtx):
    '''
    Calculate transmitter power, Ptx, from received field strength.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    Erx - Received E-field strength
    d - Distance to transmitter
    Gtx - Gain of transmitter

    Returns
    -------
    Transmitter power, Ptx
    '''

    assert isinstance(Erx, Quantity), 'Erx must be an astropy Quantity object'
    assert isinstance(d, Quantity), 'd must be an astropy Quantity object'
    assert isinstance(Gtx, Quantity), 'Gtx must be an astropy Quantity object'

    return 4. * math.pi * d ** 2 / Gtx * Erx ** 2 / R0


def Erx_from_Ptx(Ptx, d, Gtx):
    '''
    Calculate received field strength, Erx, from transmitter power.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    Ptx - Transmitter power
    d - Distance to transmitter
    Gtx - Gain of transmitter

    Returns
    -------
    Received E-field strength, Erx
    '''

    assert isinstance(Ptx, Quantity), 'Ptx must be an astropy Quantity object'
    assert isinstance(d, Quantity), 'd must be an astropy Quantity object'
    assert isinstance(Gtx, Quantity), 'Gtx must be an astropy Quantity object'

    return (Ptx * Gtx / 4. / math.pi * R0) ** 0.5 / d


def S_from_Ptx(Ptx, d, Gtx):
    '''
    Calculate power flux density, S, from transmitter power.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    Ptx - Transmitter power
    d - Distance to transmitter
    Gtx - Gain of transmitter

    Returns
    -------
    Power flux density, S (at receiver location)
    '''

    assert isinstance(Ptx, apu.Quantity), 'Ptx must be an astropy Quantity object'
    assert isinstance(d, apu.Quantity), 'd must be an astropy Quantity object'
    assert isinstance(Gtx, apu.Quantity), 'Gtx must be an astropy Quantity object'

    # log-units seem not yet flexible enough to make the simpler statement work:
    # return Gtx * Ptx / 4. / math.pi / d ** 2
    return Gtx.to(apu.Unit(1)) * Ptx.to(apu.Watt) / 4. / math.pi / d ** 2


def Ptx_from_S(S, d, Gtx):
    '''
    Calculate transmitter power, Ptx, from power flux density.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    S - Power flux density (at receiver location)
    d - Distance to transmitter
    Gtx - Gain of transmitter

    Returns
    -------
    Transmitter power, Ptx
    '''

    assert isinstance(S, Quantity), 'S must be an astropy Quantity object'
    assert isinstance(d, Quantity), 'd must be an astropy Quantity object'
    assert isinstance(Gtx, Quantity), 'Gtx must be an astropy Quantity object'

    return S.to(apu.Watt / apu.m ** 2) * 4. * math.pi * d ** 2 / Gtx.to(apu.Unit(1))


def Prx_from_S(S, f, Grx):
    '''
    Calculate received power, Prx, from power flux density.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    S - Power flux density (at receiver location)
    f - Frequency of radiation
    Grx - Gain of receiver

    Returns
    -------
    Received power, Prx
    '''

    assert isinstance(S, Quantity), 'S must be an astropy Quantity object'
    assert isinstance(f, Quantity), 'f must be an astropy Quantity object'
    assert isinstance(Grx, Quantity), 'Grx must be an astropy Quantity object'

    return S.to(apu.Watt / apu.m ** 2) * Grx.to(apu.Unit(1)) * (
        con.c ** 2 / 4. / math.pi / f ** 2
        )


def S_from_Prx(Prx, f, Grx):
    '''
    Calculate power flux density, S, from received power.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    Prx - Received power
    f - Frequency of radiation
    Grx - Gain of receiver

    Returns
    -------
    Power flux density, S (at receiver location)
    '''

    assert isinstance(Prx, Quantity), 'Prx must be an astropy Quantity object'
    assert isinstance(f, Quantity), 'f must be an astropy Quantity object'
    assert isinstance(Grx, Quantity), 'Grx must be an astropy Quantity object'

    return Prx.to(apu.Watt) / Grx.to(apu.Unit(1)) * (
        4. * math.pi * f ** 2 / con.c ** 2
        )


def free_space_loss(dist, freq):
    '''
    Calculate the free space loss of a propagating radio wave.

    Note: All quantities must be astropy Quantities (astropy.units.quantity.Quantity).

    Parameters
    ----------
    dist - Distance between transmitter and receiver
    freq - Frequency of radiation

    Returns
    -------
    Free-space loss, FSPL
    '''

    return (con.c / 4. / math.pi / freq / dist)  ** 2


# define some useful constants
R0 = 1. * (con.mu0 / con.eps0)  ** 0.5
Erx_unit = Erx_from_Ptx(1 * apu.watt, 1 * apu.km, 1 * apu.Unit(1))

# define some useful dB-Scales
dB_W = apu.dB(apu.watt)
dB_mW = apu.dB(apu.milliwatt)
db_uV_m = apu.dB(apu.microvolt ** 2 / apu.meter ** 2)


if __name__ == '__main__':
    print('This not a standalone python program! Use as module.')
