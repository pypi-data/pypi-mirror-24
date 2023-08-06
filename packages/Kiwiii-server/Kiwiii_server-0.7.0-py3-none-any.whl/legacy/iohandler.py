
from itertools import repeat, count, starmap

from chemex import molutil, v2000supplier, wclogp
from chemex.draw import calc2dcoords
from chemex.draw.svg import SVG
from tornado import web
from cheddar.data import webdataframe
from cheddar.data import excelexporter
from cheddar.basehandler import BaseHandler
from cheddar.util.multiprocess import FileBasedIPC

DL_NAME = "compound_table"


class ImportHandler(BaseHandler):
    @web.authenticated
    def post(self):
        c = self.get_arguments("cols")
        f = self.request.files['file'][0]['body']  # binary
        df_id = self.get_cookie("df")
        cols = ["_index", "_mol", "_structure"] + c
        mols = list(v2000supplier.sdf_str(f))
        if self.get_argument("implh", default=0):
            for m in mols:
                molutil.make_Hs_implicit(m)
        if self.get_argument("recalc", default=0):
            for m in mols:
                calc2dcoords.calc2dcoords(m)
        args = list(zip(mols, count(1), repeat(cols)))
        data = list(starmap(import_row, args))
        self.dfcont.update(df_id, data, cols)
        self.redirect('/')


def import_row(mol, idx, cols):
    wclogp.assign_wctype(mol)
    row = {col: str(mol.options.get(col, "")) for col in cols}
    row['_index'] = str(idx)
    row['_mol'] = mol
    row['_mw'] = molutil.mw(mol)
    row['_formula'] = molutil.formula(mol)
    row['_logp'] = wclogp.wclogp(mol)
    row['_structure'] = SVG(mol).contents()
    return row


class ExportHandler(BaseHandler):
    @web.authenticated
    def get(self):
        dol = self.get_df().dict_of_list()
        cols = self.get_df().header()
        res = FileBasedIPC(excelexporter.export)()(dol, cols)
        self.set_header("Content-Type", 'application/vnd.openxmlformats-office\
                        document.spreadsheetml.sheet; charset="utf-8"')
        self.set_header("Content-Disposition",
                        "attachment; filename={}.xlsx".format(DL_NAME))
        self.write(res.getvalue())


class OpenHandler(BaseHandler):
    @web.authenticated
    def post(self):
        df = webdataframe.loads(self.request.files['file'][0]['body'])
        id_ = self.get_cookie("df")
        self.dfcont.container[id_] = df
        self.dfcont.set_expires(id_)
        self.redirect('/')


class SaveHandler(BaseHandler):
    @web.authenticated
    def get(self):
        f = webdataframe.dumps(self.get_df())
        self.set_header("Content-Type", 'application/octet-stream')
        self.set_header("Content-Disposition",
                        "attachment; filename={}.dff".format(DL_NAME))
        self.write(f)
