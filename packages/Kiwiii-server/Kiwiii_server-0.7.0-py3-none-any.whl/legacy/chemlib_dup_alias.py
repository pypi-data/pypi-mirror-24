
import os.path
import yaml
import cheddar.data.sqliteconnection as sq
import chemex.atomtyper as at
import chemex.remover as rm
import chemex.v2000supplier as v2
import chemex.substructure as sb

SOURCE_DIR = os.path.join(os.path.dirname(__file__), "../datasource")
with open(os.path.join(SOURCE_DIR, "chemlib_info.yaml")) as f:
    CHEMLIB_INFO = yaml.load(f.read())


def gen():
    for db in CHEMLIB_INFO:
        dbpath = os.path.join(SOURCE_DIR, db['path'])
        sq.CON.connect(os.path.normpath(dbpath), db['table'])
        pkey_idx = sq.CON.columns.index(db["primary_key"])
        strcol_idx = sq.CON.columns.index(db["structure_column"])
        for rec in sq.CON:
            mol = v2.sdf_str_first(rec[strcol_idx])
            at.assign_hydrogen(mol)
            rm.remove_water(mol)
            rm.remove_salt(mol)
            yield (rec[pkey_idx], mol)

sortedit = iter(sorted(gen(), key=lambda x: x[1].mw()))
res = []
stack = [next(sortedit)]
for curr in sortedit:
    if curr[1].mw() == stack[0][1].mw():
        for s in stack:
            if sb.equal(curr[1], s[1]):
                res.append("{}\t{}\n".format(s[0], curr[0]))
                res.append("{}\t{}\n".format(curr[0], s[0]))
        stack.append(curr)
    else:
        stack = [curr]

savepath = os.path.join(SOURCE_DIR, "./aliases_tsv/chemlib_alias.tsv")
with open(savepath, "w+") as f:
    f.write("".join(res))
