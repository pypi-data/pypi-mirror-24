
import pickle
from itertools import repeat, count, starmap

from chemex.draw import calc2dcoords
from chemex.draw.svg import SVG
from chemex import mcsdr, molutil, substructure, wclogp
from chemex import smilessupplier, v2000supplier
try:
    from chemex import rdkit
    RDK_AVAILABLE = True
except ImportError:
    RDK_AVAILABLE = False
from tornado import web

from cheddar.basehandler import BaseHandler
from cheddar.data.sqliteconnection import Connection
from cheddar.worker import Worker

CONN = Connection("./datasource/chemlib.sqlite3")
MASTER = []
INVISIBLES = ("_mol",)
UNSEARCHABLES = ("_mol", "_structure")
CALCULATED = ("_mw", "_formula", "_logp", "_aliases")
for r in CONN.rows_iter(("MASTER",), orderby=("id",)):
    cols = [c for c in CONN.columns(r["db"]) if c not in UNSEARCHABLES]
    MASTER.append({"db": r["db"], "name": r["name"], "cols": cols})

RES_CONN = Connection("./datasource/results.sqlite3")
RES_MASTER = []
for r in RES_CONN.rows_iter(("MASTER",), orderby=("id",)):
    tags = [t for t in r["tags"].split("\t")]
    RES_MASTER.append({"tab": r["tab"], "name": r["name"],
                       "cols": RES_CONN.columns(r["tab"]),
                       "tags": tags, "desc": r["description"]})


class DfWorker(Worker):
    """ Multi-process worker for row by row task processing """
    def __init__(self, args, func, args_size, dfcont, df_id):
        super().__init__(args, func, args_size)
        self.dfcontainer = dfcont
        self.df_id = df_id
        self._data = []

    def on_task_done(self, res):
        if res is not None:
            self._data.append(res)

    def on_finish(self):
        if self._data:
            data = sorted(self._data, key=lambda x: x["_index"])
            self.dfcontainer.update(self.df_id, data)


"""
Row task functions for starmap and DfWorker
"""


def process_row(idx, row, mol):
    """ Base task """
    row['_index'] = idx
    row["_mol"] = mol
    row["_structure"] = SVG(mol).contents()
    row["_mw"] = molutil.mw(mol)
    row["_formula"] = molutil.formula(mol)
    row["_logp"] = wclogp.wclogp(mol)
    row["_aliases"] = aliases(row["ID"], mol)


def aliases(id_, mol):
    dbs = [t["db"] for t in MASTER]
    cur = (CONN.find_iter("_mw_wo_sw", molutil.mw_wo_sw(mol), dbs))
    res = []
    for r in cur:
        if id_ != r["ID"] and r["_mw_wo_sw"] != 0\
                 and substructure.equal(mol, pickle.loads(r["_mol"])):
            res.append(r["ID"])
    if res:
        return ", ".join(res)
    return ""


def pick_row(idx, row):
    mol = pickle.loads(row["_mol"])
    process_row(idx, row, mol)
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


class MainHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.dfcont.remove_expired()
        cols = [c for c in self.get_df().columns() if c not in INVISIBLES]
        self.render("main.html", headers=self.get_df().header(), libs=MASTER,
                    assays=RES_MASTER, cols=cols, rdk=RDK_AVAILABLE)


class PickHandler(BaseHandler):
    @web.authenticated
    def post(self):
        tbl = self.get_argument("db")
        qs = self.get_argument("queries").split("\n")
        res = (dict(CONN.find_first("ID", q.strip(), (tbl,), 1)) for q in qs)
        args = zip(count(1), res)
        data = list(starmap(pick_row, args))
        cols = ["_index", "_mol", "_structure"]
        cols.extend(CALCULATED)
        cols.extend(c for c in CONN.columns(tbl) if c not in cols)
        df_id = self.get_cookie("df")
        self.dfcont.update(df_id, data, cols)
        self.redirect('/')


class AssayHandler(BaseHandler):
    @web.authenticated
    def post(self):
        # TODO: filter (ex. remove invalid)
        tbls = [t["db"] for t in MASTER]
        cols = ["_index", "_mol", "_structure", "ID"]
        cols.extend(CALCULATED)
        hide = []  # mol attrs are invisible by default
        for tbl in tbls:
            hide.extend(c for c in CONN.columns(tbl) if c not in hide)
        cols.extend(h for h in hide if h not in cols)
        assays = self.get_arguments("assays")
        for a in assays:
            cols.extend(c for c in RES_CONN.columns(a) if c not in cols)
        rows = []
        for r in RES_CONN.rows_iter(assays):
            row = {h: "" for h in hide}  # fill empty mol attrs columns
            row.update(dict(CONN.find_first("ID", r["ID"], tbls, 1)))
            row.update(dict(r))
            rows.append(row)
        args = zip(count(1), rows)
        data = list(starmap(pick_row, args))
        df_id = self.get_cookie("df")
        self.dfcont.update(df_id, data, cols)
        self.redirect('/')


class AdvancedSearchHandler(BaseHandler):
    @web.authenticated
    def post(self):
        qcol = self.get_argument("column")
        query = self.get_argument("query")
        cd = self.get_argument("condition")
        if cd == "in":
            qs = query.split("\n")
            query = [q.strip() for q in qs]
        dbs = self.get_arguments("dbs")
        cd_map = {"eq": "=", "gt": ">", "lt": "<", "ge": ">=", "le": "<=",
                  "lk": "LIKE", "in": "IN"}
        res = (dict(r) for r in CONN.find_iter(qcol, query, dbs, cd_map[cd]))
        args = zip(count(1), res)
        data = list(starmap(pick_row, args))
        cols = ["_index", "_mol", "_structure"]
        cols.extend(CALCULATED)
        for tbl in dbs:
            cols.extend(c for c in CONN.columns(tbl) if c not in cols)
        df_id = self.get_cookie("df")
        self.dfcont.update(df_id, None, cols)
        if data:
            self.dfcont.update(df_id, data)
        self.redirect('/')


class SubstructureHandler(BaseHandler):
    @web.authenticated
    def post(self):
        dbs = self.get_arguments("dbs")
        cols = ["_index", "_mol", "_structure"]
        cols.extend(CALCULATED)
        for tbl in dbs:
            cols.extend(c for c in CONN.columns(tbl) if c not in cols)
        # generate query mol
        format_ = self.get_argument("format")
        query = self.get_argument("query", strip=False).replace("\r\n", "\n")
        if format_ == "smiles":
            qmol = smilessupplier.smiles_to_compound(query)
            calc2dcoords.calc2dcoords(qmol)
        elif format_ == "molfile":
            qmol = v2000supplier.sdf_str_first(query)
        elif format_ == "dbid":
            qdb = self.get_argument("qdb")
            qmol = pickle.loads(CONN.find_first("ID", query, (qdb,))["_mol"])
        # generate array
        type_ = self.get_argument("type")
        if type_ == "exact":
            cur = (CONN.find_iter("_mw_wo_sw", molutil.mw_wo_sw(qmol), dbs))
            rows = [dict(r) for r in cur]
            rlen = len(rows)
            args = zip(count(1), rows, repeat(qmol))
        elif type_ in ("super", "sub"):
            # TODO: mw filter for substr and supstr ?
            rows = (dict(r) for r in CONN.rows_iter(dbs))
            rlen = CONN.rows_count(dbs)
            args = zip(count(1), rows, repeat(qmol))
        elif type_ in ("mcsdr", "gls"):
            diam = int(self.get_argument("diam"))
            tree = int(self.get_argument("tree"))
            skip = int(self.get_argument("skip"))
            if type_ == "mcsdr":
                mcs = int(self.get_argument("mcs"))
                opt = (diam, tree, mcs, skip)
                cols.append("_mcsdr_size")
            else:
                sim = float(self.get_argument("sim"))
                opt = (diam, tree, sim, skip)
                cols.append("_similarity")
            qmol = mcsdr.comparison_array(qmol)
            rows = (dict(r) for r in CONN.rows_iter(dbs))
            rlen = CONN.rows_count(dbs)
            args = zip(count(1), rows, repeat(qmol), repeat(opt))
        elif type_ == "morgan":
            sim = float(self.get_argument("sim"))
            cols.append("_similarity")
            rows = (dict(r) for r in CONN.rows_iter(dbs))
            rlen = CONN.rows_count(dbs)
            args = zip(count(1), rows, repeat(qmol), repeat(sim))
        func = {"exact": exmatch_row, "sub": substr_row,
                "super": supstr_row, "mcsdr": mcsdr_row,
                "gls": gls_row, "morgan": morgan_row}
        df_id = self.get_cookie("df")
        self.dfcont.update(df_id, None, cols)
        worker = DfWorker(args, func[type_], rlen, self.dfcont, df_id)
        self.wqueue.put(df_id, worker)
        self.redirect('/')


class StructurePreviewHandler(web.RequestHandler):
    def post(self):
        format_ = self.get_argument("format")
        query = self.get_argument("query", strip=False)
        if format_ == "dbid":
            qdb = self.get_argument("qdb")
            res = CONN.find_first("ID", query, (qdb,))
            if res is None:
                self.write('<span class="msg_warn">Not found</span>')
            else:
                mol = pickle.loads(res["_mol"])
                self.write(SVG(mol).contents())
        else:
            try:
                if format_ == "smiles":
                    mol = smilessupplier.smiles_to_compound(query)
                    calc2dcoords.calc2dcoords(mol)
                elif format_ == "molfile":
                    mol = v2000supplier.sdf_str_first(query)
            except ValueError:
                self.write('<span class="msg_warn">Format Error</span>')
            else:
                self.write(SVG(mol).contents())


class MergeHandler(BaseHandler):
    @web.authenticated
    def post(self):
        ids = self.get_df()["ID"]
        assay_cols = self.get_arguments("cols")
        data = {}
        data["newID"] = [i for i in ids]
        for assay_col in assay_cols:
            assay, col = assay_col.split(":")
            data[assay_col] = []
            for id_ in ids:
                res = RES_CONN.find_first("ID", id_, (assay,))
                try:
                    data[assay_col].append(res[col])
                except TypeError:  # res = None
                    data[assay_col].append("")
        self.get_df()["ID"].merge("newID", data, ["newID"] + assay_cols)
        self.redirect('/')
