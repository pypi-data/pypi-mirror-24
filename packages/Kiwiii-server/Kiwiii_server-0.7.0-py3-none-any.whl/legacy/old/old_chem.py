# coding: UTF-8

"""
Chemical structure renderer module
"""

import math
import traceback
import io

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdMolDescriptors

from tmp import image


BOND_LENGTH = 1.54  # standard C-C bond length (Å)


class MoleculeStructureKey(object):
    pass


def molblocks_to_mols(molblocks):
    """Convert MOLfile format text to rdkit.Chem.rdchem.Mol

    Args:
      molblocks: {id: molblock, ...}
    Returns:
      {id: mol, ...}
    """
    mols = {}
    for k, v in molblocks.items():
        mols[k] = Chem.MolFromMolBlock(str(v))
    return mols


def render_molecule_rdk(mol, size=(250, 250)):
    """Generate a structure image from rdkit.Chem.rdchem.Mol.
    The generated image is a bytearray of PNG format data.

    Args:
      mols: {key: mol, ...}
    Returns:
      {key: image, ...}
    """
    if mol is None:
        return image.render_text("No Structure", size)
    opt = Draw.DrawingOptions()
    opt.coordScale = _calc_scaling_factor(mol)
    try:
        raw_img = Draw.MolToImage(mol, size, True, True, True, opt)
        buf = io.StringIO()
        raw_img.save(buf, format="PNG")
        mol_img = bytearray(buf.getvalue())
        buf.close()
    except:
        print(traceback.format_exc())
        mol_img = image.render_text("No Structure", size)
    return mol_img


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


def render_molecules_cdk(mols, size=(250, 250)):
    """Generate structure image from MOLfile format texts.
    The generated image is a bytearray of PNG format data.

    Args:
      mols: {key: molblock, ...}
    Returns:
      {key: image, ...}
    """
    from tmp.java import CONNECTION
    if not CONNECTION.is_alive():
        raise Exception("No JavaGataway Connection.")
    mol_imgs = {}
    for k, v in mols.items():
        if v is None:
            mol_imgs[k] = image.render_text("No Structure", size)
            continue
        mol_img = CONNECTION.renderMolecule(v)
        if mol_img == "":
            mol_imgs[k] = image.render_text("No Structure", size)
            continue
        mol_imgs[k] = mol_img
    CONNECTION.kill()
    return mol_imgs


def get_smiles(mol):
    """Get kekule SMILES
    Args: rdkit.Chem.rdchem.Mol
    Returns: kekule SMILES
    """
    smiles = None
    try:
        Chem.Kekulize(mol)
        smiles = Chem.MolToSmiles(mol, isomericSmiles=True, kekuleSmiles=True)
    except:
        print(traceback.format_exc())
    return smiles


def get_molformula(mol):
    """Get molecule formula
    Args: rdkit.Chem.rdchem.Mol
    Returns: formula
    """
    try:
        return rdMolDescriptors.CalcMolFormula(mol)
    except:
        print(traceback.format_exc())
        return "N/A"


def get_molwt(mol):
    """Get molecular weight
    Args: rdkit.Chem.rdchem.Mol
    Returns: molecular weight
    """
    try:
        return "{0:.2f}".format(round(rdMolDescriptors._CalcMolWt(mol), 2))
    except:
        print(traceback.format_exc())
        return "N/A"


def get_num_acceptor(mol):
    """Get total number of oxygen and nitrogen (Lipinski HBA)
    Args: rdkit.Chem.rdchem.Mol
    Returns: Lipinski HBA
    """
    try:
        return str(rdMolDescriptors.CalcNumLipinskiHBA(mol))
    except:
        print(traceback.format_exc())
        return "N/A"


def get_num_donor(mol):
    """Get total number of oxygen and nitrogen (Lipinski HBD)
    Args: rdkit.Chem.rdchem.Mol
    Returns: Lipinski HBD
    """
    try:
        return str(rdMolDescriptors.CalcNumLipinskiHBD(mol))
    except:
        print(traceback.format_exc())
        return "N/A"


def scan_sdf(path):
    """Scan sdfile to get list of properties

    Args:
      path: SDFile path
    Returns:
      list of properties
    """
    sup = Chem.SDMolSupplier(str(path))
    input_cols = set()
    while not sup.atEnd():
        mol = sup.next()
        input_cols.update(set(mol.GetPropNames()))
    return


def read_sdf(path, cols):
    """Read and parse selected column in SDFile

    Args:
      path: SDFile path
      cols: list of columns to be read
    Returns:
      dataframe
    """
    sup = Chem.SDMolSupplier(str(path))
    input_rcds = []
    input_cols = set()
    cnt = 0
    while not sup.atEnd():
        mol = sup.next()
        input_cols.update(set(mol.GetPropNames()))
    sup.reset()
    while not sup.atEnd():
        mol = sup.next()
        prop = {"Index": str(cnt)}
        cnt += 1
        prop["Mol"] = mol
        for col in input_cols:
            try:
                prop[col] = str(mol.GetProp(col))
            except:
                prop[col] = "N/A"
        input_rcds.append(prop)
    output_cols = ["Index", "Mol"]
    output_cols.extend(list(input_cols))
    output_cols = map(to_unicode, output_cols)
    output_rcds = map(dict_to_unicode, input_rcds)
    return output_rcds, output_cols


def write_sdf(mol, path):
    writer = Chem.SDWriter(path)
    writer.write(mol)
    writer.close()


def to_unicode(string):
    encodings = ['shift_jis', ]
    decoded = string
    for e in encodings:
        try:
            decoded = string.decode(e)
            break
        except:
            pass
    return decoded


def dict_to_unicode(dict_):
    return {to_unicode(k): to_unicode(v) for k, v in dict_.items()}
