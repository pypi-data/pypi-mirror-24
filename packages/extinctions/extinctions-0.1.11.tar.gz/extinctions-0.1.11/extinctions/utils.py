"""Some utilities."""

import pylab as P
import numpy as N
import seaborn


def from_ebv_sfd_to_sdss_albd(ebv):
    """Return A(lbd) for the 5 SDSS filters: u, g, r, i, z."""
    coeff = {'u': 5.155, 'g': 3.793, 'r': 2.751, 'i': 2.086, 'z': 1.479}
    return {f: coeff[f] * ebv for f in coeff}


def from_sdss_albd_to_megacam_albd(sdss):
    """Return A(lbd) for the 6 Megecam filters: u, g, r, i_old, i_new, z."""
    megacam = {}
    megacam['u'] = sdss['u'] - 0.241 * (sdss['u'] - sdss['g'])
    megacam['g'] = sdss['g'] - 0.153 * (sdss['g'] - sdss['r'])
    megacam['r'] = sdss['r'] - 0.024 * (sdss['g'] - sdss['r'])
    megacam['z'] = sdss['z'] - 0.074 * (sdss['i'] - sdss['z'])
    megacam['i_old'] = sdss['i'] - 0.085 * (sdss['r'] - sdss['i'])
    megacam['i_new'] = sdss['i'] - 0.003 * (sdss['r'] - sdss['i'])
    return megacam


def from_ebv_sfd_to_megacam_albd(ebv):
    """Return A(lbd) for the 6 Megacam filters: u, g, r, i, z."""
    return from_sdss_albd_to_megacam_albd(from_ebv_sfd_to_sdss_albd(ebv))


def plots(ra, dec, ebv, albd, title=None, figname="", filters=None):
    """Make some plots."""
    fig = P.figure()
    ax = fig.add_subplot(111, xlabel='RA (deg)', ylabel='DEC (deg)')
    scat = ax.scatter(ra, dec, c=ebv, cmap=(P.cm.jet))
    cb = fig.colorbar(scat)
    cb.set_label('E(B-V)')
    if title is not None:
        ax.set_title(title)
    fig.savefig(figname + "_ebmv_map.png")

    if filters is None:
        filters = albd.keys()
    fig = P.figure()
    ax = fig.add_subplot(111, xlabel='A(lbd)', ylabel='#')
    for f in filters:
        ax.hist(albd[f], histtype='step', lw=2, label='<%s>=%.2f' %
                (f, N.mean(albd[f])))
    if title is not None:
        ax.set_title(title)
    ax.legend(loc='best')
    fig.savefig(figname + "_albd.png")

    P.show()
