# coding: UTF-8
import os
import sys
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor
from PySide import QtGui

app = QtGui.QApplication(sys.argv)
mol = Chem.MolFromSmiles('c1c(C[15NH3+])ccnc1[C@](Cl)(Br)[C@](Cl)(Br)F')
#'CCC(CC)O[C@@H]1C=C(C[C@@H]([C@H]1NC(=O)C)[NH3+])C(=O)OCC')
rdDepictor.Compute2DCoords(mol)
# os.environ['RDKIT_CANVAS']='sping'
# img = Draw.MolToImage(mol, (300, 300))
# img.save("hoge_sping.png")
pixmap = Draw.MolToQPixmap(mol, size=(300, 300), kekulize=False)
pixmap.save("hoge.png")