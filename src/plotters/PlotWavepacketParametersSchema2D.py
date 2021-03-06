r"""The WaveBlocks Project

Plot the evolution of the parameters :math:`Pi_i = (q, p, Q, P, S)`
of a homogeneous or inhomogeneous Hagedorn wavepacket during the
time propagation.

@author: R. Bourquin
@copyright: Copyright (C) 2012 R. Bourquin
@license: Modified BSD License
"""

import sys
from numpy import array, squeeze, linspace, dot, sin, cos, pi, transpose
from matplotlib.pyplot import *
from WaveBlocksND import IOManager

import GraphicsDefaults as GD


def read_all_datablocks(iom):
    r"""Read the data from all blocks that contain any usable data.

    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    """
    # Iterate over all blocks and plot their data
    for blockid in iom.get_block_ids():
        if iom.has_wavepacket(blockid=blockid):
            plot_parameters(read_data_homogeneous(iom, blockid=blockid), index=blockid)
        elif iom.has_inhomogwavepacket(blockid=blockid):
            plot_parameters(read_data_inhomogeneous(iom, blockid=blockid), index=blockid)
        else:
            print("Warning: Not plotting wavepacket parameters in block '"+str(blockid)+"'!")


def read_data_homogeneous(iom, blockid=0):
    r"""
    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    :param blockid: The data block from which the values are read.
    """
    parameters = iom.load_parameters()
    timegrid = iom.load_wavepacket_timegrid(blockid=blockid)
    time = timegrid * parameters["dt"]

    Pi = iom.load_wavepacket_parameters(blockid=blockid)

    # The Dimension D, we know that q has shapw (#timesteps, D, 1)
    D = Pi[0].shape[1]
    if not D == 2:
        print("Warning: Trajectory plotting implemented only for 2D wavepackets")
        return

    Pi = map(squeeze, Pi)
    qhist, phist, Qhist, Phist, Shist = Pi
    return (time, [qhist], [phist], [Qhist], [Phist], [Shist])


def read_data_inhomogeneous(iom, blockid=0):
    r"""
    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    :param blockid: The data block from which the values are read.
    """
    parameters = iom.load_parameters()
    timegrid = iom.load_inhomogwavepacket_timegrid(blockid=blockid)
    time = timegrid * parameters["dt"]

    Pis = iom.load_inhomogwavepacket_parameters(blockid=blockid)

    # The Dimension D, we know that q_0 has shapw (#timesteps, D, 1)
    D = Pis[0][0].shape[1]
    if not D == 2:
        print("Warning: Trajectory plotting implemented only for 2D wavepackets")
        return

    # List with Pi time evolutions
    Phist = []
    Qhist = []
    Shist = []
    phist = []
    qhist = []

    for q,p,Q,P,S in Pis:
        qhist.append(squeeze(q))
        phist.append(squeeze(p))
        Qhist.append(squeeze(Q))
        Phist.append(squeeze(P))
        Shist.append(squeeze(S))

    return (time, qhist, phist, Qhist, Phist, Shist)


def plot_parameters(data, index=0):
    r"""Plot the data parameters :math:`(q,p,Q,P,S)` over time.
    For each new `index` we start a new figure. This allows plotting
    several time evolutions to the same figure
    """
    print("Plotting the parameters of data block '"+str(index)+"'")

    timegrid, qhist, phist, Qhist, Phist, Shist = data

    r = 1.0
    theta = linspace(0, 2*pi, 64)
    circle = array([r*cos(theta), r*sin(theta)])

    # Plot the 2D trajectory of the parameters q and p
    fig = figure()
    ax = fig.gca()

    for qitem, Qitem in zip(qhist, Qhist):
        for q, Q in zip(qitem, Qitem):
            C = q.reshape((-1,1)) + dot(Q, circle)
            ax.plot(q[0], q[1], "bo")
            ax.plot(C[0,:], C[1,:], "b-")

    ax.set_xlabel(r"$q_x$")
    ax.set_ylabel(r"$q_y$")
    ax.grid(True)
    ax.set_title(r"Schematic evolution of $q$ and $Q$")
    fig.savefig("wavepacket_parameters_schema_pos_block"+str(index)+GD.output_format)
    close(fig)


    fig = figure()
    ax = fig.gca()
    for pitem, Pitem in zip(phist, Phist):
        for p, P in zip(pitem, Pitem):
            C = p.reshape((-1,1)) + dot(P, circle)
            ax.plot(p[0], p[1], "bo")
            ax.plot(C[0,:], C[1,:], "b-")
    ax.set_xlabel(r"$p_x$")
    ax.set_ylabel(r"$p_y$")
    ax.grid(True)
    ax.set_title(r"Schematic evolution of $p$ and $P$")
    fig.savefig("wavepacket_parameters_schema_mom_lock"+str(index)+GD.output_format)
    close(fig)




if __name__ == "__main__":
    iom = IOManager()

    # Read file with simulation data
    try:
        iom.open_file(filename=sys.argv[1])
    except IndexError:
        iom.open_file()

    # Read the data and plot it, one plot for each data block.
    read_all_datablocks(iom)

    iom.finalize()
