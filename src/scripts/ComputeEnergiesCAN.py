"""The WaveBlocks Project

Compute the energies of the different wavepackets or wavefunctions.

@author: R. Bourquin
@copyright: Copyright (C) 2010, 2011, 2012, 2013 R. Bourquin
@license: Modified BSD License
"""

import argparse

from WaveBlocksND import IOManager
from WaveBlocksND import GlobalDefaults as GD

parser = argparse.ArgumentParser()

parser.add_argument("simfile",
                    type = str,
                    help = "The simulation data file",
                    nargs = "?",
                    default = GD.file_resultdatafile)

parser.add_argument("-b", "--blockid",
                    help = "The data block to handle",
                    nargs = "*",
                    default = [0])

# TODO: Filter type of objects
# parser.add_argument("-t", "--type",
#                     help = "The type of objects to consider",
#                     type = str,
#                     default = "all")

args = parser.parse_args()

# Read file with simulation data
iom = IOManager()
iom.open_file(filename=args.simfile)

# Which blocks to handle
if "all" in args.blockid:
    blocks_to_handle = iom.get_block_ids()
else:
    blocks_to_handle = map(int, args.blockid)

# Iterate over all blocks
for blockid in blocks_to_handle:
    print("Computing the energies in data block '"+str(blockid)+"'")

    if iom.has_energy(blockid=blockid):
        print("Datablock '"+str(blockid)+"' already contains energy data, silent skip.")
        continue

    # NOTE: Add new algorithms here

    if iom.has_wavepacket(blockid=blockid):
        import EnergiesWavepacket
        EnergiesWavepacket.compute_energy_hawp(iom, blockid=blockid, eigentrafo=False, iseigen=False)
    elif iom.has_wavefunction(blockid=blockid):
        import EnergiesWavefunction
        EnergiesWavefunction.compute_energy(iom, blockid=blockid, eigentrafo=False, iseigen=False)
    elif iom.has_inhomogwavepacket(blockid=blockid):
        import EnergiesWavepacket
        EnergiesWavepacket.compute_energy_inhawp(iom, blockid=blockid, eigentrafo=False, iseigen=False)
    else:
        print("Warning: Not computing any energies in block '"+str(blockid)+"'!")

iom.finalize()
