
# Copyright (C) 2014-2016 by Seiji Matsuoka
# All Rights Reserved.

import json
import operator
import pickle
import re
from chemex.draw.svg import SVG
from chemex import mcsdr, molutil, substructure, wclogp
try:
    from chemex import rdkit
    RDK_AVAILABLE = True
except ImportError:
    RDK_AVAILABLE = False

from cheddar.sqliteconnection import Connection

CHEMLIB_PATH = "./datasource/chemlib.sqlite3"

CALC = {
    "_mw": molutil.mw,
    "_formula": molutil.formula,
    "_logp": wclogp.wclogp
}


def like_operator(a, b):
    return re.match(b.replace("%", ".*?").replace("_", "[\w ]"), a) is not None


def is_rdk_available():
    return RDK_AVAILABLE


def process_row(idx, row, mol):
    """ Base task """
    row["_index"] = idx
    row["_structure"] = SVG(mol).contents()
    row["_mol"] = json.dumps(mol.jsonized())
    for c, f in CALC.items():
        row[c] = f(mol)


def aliases(mol, id_=None):
    conn = Connection(CHEMLIB_PATH)
    dbs = [table["table"] for table in conn.document()["tables"]]
    cur = (conn.find_iter("_mw_wo_sw", molutil.mw_wo_sw(mol), dbs))
    res = []
    for r in cur:
        if id_ == r["ID"] or not r["_mw_wo_sw"]:  # itself or no structure
            continue
        if substructure.equal(mol, pickle.loads(r["_mol"])):
            res.append(r["ID"])
    if res:
        return ", ".join(res)


def plain_row(idx, row):
    row["_index"] = idx
    return row


def pick_row(idx, row):
    mol = pickle.loads(row["_mol"])
    process_row(idx, row, mol)
    row["_aliases"] = aliases(mol, row["ID"])
    return row


def prop_row(idx, row, filter_):
    mol = pickle.loads(row["_mol"])
    col, cd, query, qtype = filter_
    qconv = {"numeric": float, "text": str}
    query = [qconv[qtype](q) for q in query]
    if cd != "in":
        query = query[0]
    conv = {
        "eq": operator.eq, "gt": operator.gt, "lt": operator.lt,
        "ge": operator.ge, "le": operator.le,
        "lk": like_operator, "in": lambda a, b: a in b}
    if conv[cd](CALC[col](mol), query):
        process_row(idx, row, mol)
        return row


def import_row(mol, idx, cols):
    row = {col: str(mol.options.get(col, "")) for col in cols}
    process_row(idx, row, mol)
    row["_aliases"] = aliases(mol)
    return row


def exmatch_row(idx, row, qmol):
    mol = pickle.loads(row["_mol"])
    if substructure.equal(qmol, mol):
        process_row(idx, row, mol)
        return row


def substr_row(idx, row, qmol):
    mol = pickle.loads(row["_mol"])
    if substructure.substructure(mol, qmol):
        process_row(idx, row, mol)
        return row


def supstr_row(idx, row, qmol):
    mol = pickle.loads(row["_mol"])
    if substructure.substructure(qmol, mol):
        process_row(idx, row, mol)
        return row


def mcsdr_row(idx, row, qm_arr, param):
    mol = pickle.loads(row["_mol"])
    diam, tree, thld, skip = param
    if len(mol) > skip:  # mol size filter
        return
    try:
        arr = mcsdr.comparison_array(mol, diam, tree)
    except ValueError:
        return
    size = mcsdr.mcsdr_size(arr, qm_arr)
    if size >= thld:
        process_row(idx, row, mol)
        row['_mcsdr_size'] = size
        return row


def gls_row(idx, row, qm_arr, param):
    mol = pickle.loads(row["_mol"])
    diam, tree, thld, skip = param
    if len(mol) > skip:  # mol size filter
        return
    try:
        arr = mcsdr.comparison_array(mol, diam, tree)
    except ValueError:
        return
    sim = mcsdr.gls_index(arr, qm_arr)
    if sim >= thld:
        process_row(idx, row, mol)
        row['_similarity'] = sim
        return row


def morgan_row(idx, row, qmol, thld):
    mol = pickle.loads(row["_mol"])
    sim = rdkit.morgan_similarity(mol, qmol, 4)
    if sim >= thld:
        process_row(idx, row, mol)
        row['_similarity'] = sim
        return row


def gls_matrix(row, arr1, arr2, thld):
    dist = mcsdr.gls_dist(arr1, arr2)
    if dist <= thld:
        row['dist'] = dist
        return row


def morgan_matrix(row, mol1, mol2, thld):
    dist = round(1 - rdkit.morgan_similarity(mol1, mol2), 2)
    if dist <= thld:
        row['dist'] = dist
        return row
