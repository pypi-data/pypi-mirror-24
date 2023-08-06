
import math

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor
from rdkit.Chem import rdMolTransforms

mol = Chem.MolFromSmiles(
    'CCC(CC)O[C@@H]1C=C(C[C@@H]([C@H]1NC(=O)C)[NH3+])C(=O)OCC')
rdDepictor.Compute2DCoords(mol)
conf = mol.GetConformer()
for bond in mol.GetBonds():
    print bond.GetIdx()
    a = bond.GetBeginAtom()
    b = bond.GetEndAtom()
    print a.GetSymbol(), b.GetSymbol()
    apos = conf.GetAtomPosition(a.GetIdx())
    bpos = conf.GetAtomPosition(b.GetIdx())
    print math.sqrt((apos[0] - bpos[0]) ** 2 + (apos[1] - bpos[1]) ** 2)


##for i in range(mol.GetNumAtoms() - 1):
#    print mol.GetAtomWithIdx(i).GetSymbol()
#    print [round(conf.GetAtomPosition(i)[0], 2), round(
#        conf.GetAtomPosition(i)[0], 2)]
#    print rdMolTransforms.GetBondLength(conf, i, i + 1)
#Draw.MolToFile(mol, 'mol.png')
