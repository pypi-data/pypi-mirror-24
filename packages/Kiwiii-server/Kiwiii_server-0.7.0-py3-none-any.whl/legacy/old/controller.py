# coding: UTF-8
import exception

from tmp import old_chem, sqlite


class Controller():
    """Get queries from GUI and process data to store cheddar.data.table"""

    def __init__(self, table):
        self._table = table
        self._jcon = None

    def import_db(self, db, ids, renderer):
        """Import compounds from sqlite database

        Returns:
          a number of records obtained
        Raises:
          SQLiteConnectionError(sqlite)
        """
        self._table.init_df(ids, ["ID", ])
        con = sqlite.Connection(table=db)
        molblocks = con.find_structures_by_ids(ids)
        mols = old_chem.molblocks_to_mols(molblocks)
        self._table.join("ID", "Mol", mols)
        if renderer == "CDK":
            mol_imgs = old_chem.render_molecules_cdk(molblocks)
            self._table.join("ID", "Structure", mol_imgs)
        elif renderer == "RDKit":
            self._table.calc("Mol", old_chem.render_molecule_rdk, "Structure")
        names = con.find_by_ids(ids, "name")
        if names is not None:
            self._table.join("ID", "Name", names)
        return self._table.row_count()

    def add_prop(self):
        """Add molecule properties"""
        self._table.calc("Mol", old_chem.get_molwt, "MW")
        self._table.calc("Mol", old_chem.get_molformula, "Formula")
        self._table.calc("Mol", old_chem.get_smiles, "SMILES")

    def show_lalist(self):
        """Get the list of logical assay in Genedata Screener

        Raises:
          JavaConnectionError(java)
        """
        from tmp.java import CONNECTION
        if not CONNECTION.is_alive():
            CONNECTION.restart()
        return CONNECTION.get_logical_assays()

    def add_drc(self, reportkey, reportname, options):
        """Get dose-response curves in Genedata Screener

        Args:
          reportkey: LogicalAssayReportKey object
          reportname: logical assay name
          options: cheddar.java.DRCOptions
        Raises:
          JavaConnectionError
        """
        from tmp.java import CONNECTION
        if not CONNECTION.is_alive():
            raise exception.JavaConnectionError
        ids = self._table.column("ID")
        drc_data = CONNECTION.get_drc_data(reportkey, ids, options)
        CONNECTION.kill()
        self._table.join("ID", reportname, drc_data[0])
        self._table.join("ID", "AC50", drc_data[1])
        self._table.join("ID", "nHill", drc_data[2])

    def import_sdf(self, path):
        """Open SDFile and set to data

        Args:
          path: file to be read
        """
        data, columns = old_chem.read_sdf(path)
        self._table.init_df(columns=columns)
        for row in data:
            self._table.append_row(row)
        self._table.calc("Mol", old_chem.render_molecule_rdk, "Structure")
        columns.insert(2, "Structure")
        self._table.df = self._table.df[columns]
        return self._table.row_count()
