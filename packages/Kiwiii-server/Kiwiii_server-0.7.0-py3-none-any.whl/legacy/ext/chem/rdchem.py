
"""
Chemical structure renderer module
"""

import math
from rdkit.Chem import Draw

BOND_LENGTH = 1.54  # standard C-C bond length (Å)


def render_molecule(mol, size=(250, 250)):
    """Generate a structure image from rdkit.Chem.rdchem.Mol.
    The generated image is a bytearray of PNG format data.

    Args:
      mols: {key: mol, ...}
    Returns:
      {key: image, ...}
    """
    opt = Draw.DrawingOptions()
    opt.coordScale = _calc_scaling_factor(mol)
    pixmap = Draw.MolToQPixmap(mol, size, True, True, True, opt)
    return pixmap


def _calc_scaling_factor(mol):
    """Calculate scaling factor in molecule drawing
    to correct irregular bond length in MOLfile.

    Args:
      mol: rdkit.Chem.rdchem.Mol
    Returns:
      scaling factor(float)
    """
    conf = mol.GetConformer()
    bonds = mol.GetBonds()
    if not bonds:
        return 1
    dists = []
    for bond in bonds:
        apos = conf.GetAtomPosition(bond.GetBeginAtom().GetIdx())
        bpos = conf.GetAtomPosition(bond.GetEndAtom().GetIdx())
        dist = math.sqrt(
            (apos[0] - bpos[0]) ** 2 + (apos[1] - bpos[1]) ** 2)
        dists.append(dist)
    avg = sum(dists) / len(bonds)  # There may be a better way
    return BOND_LENGTH / avg
