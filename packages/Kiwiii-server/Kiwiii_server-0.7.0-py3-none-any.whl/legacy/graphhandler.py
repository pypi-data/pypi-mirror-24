
from itertools import combinations
import json

from chemex.draw.svg import SVG
from chemex.mcsdr import comparison_array, mp_gls_dist
try:
    from chemex import rdkit
except ImportError:
    pass
import networkx as nx
from tornado import web

from cheddar.basehandler import BaseHandler
from cheddar.worker import Worker


def csmap_args(supplier, cs_diameter, cs_size, max_num_atoms):
    arrs = []
    for i, mol in enumerate(supplier):
        if len(mol) > max_num_atoms:
            arr = ([], 0, {})
        else:
            arr = comparison_array(mol, cs_diameter, cs_size)
        arrs.append((i, arr, mol))
    arrsize = len(arrs)
    args_length = int(arrsize * (arrsize - 1) / 2)
    args = ((i[0], j[0], i[1], j[1]) for i, j in combinations(arrs, 2))
    return arrs, args, args_length


def csmap_single_core(args, dist_threshold):
    G = nx.Graph()
    arrs, args, alen = args
    for i, _, c in arrs:
        G.add_node(i, elem=c, type="node")
    for arg in args:
        u, v, d = mp_gls_dist(*arg)
        if d < dist_threshold:
            G.add_edge(u, v, dist=d)
    return G


def graph_to_json(df):
    """convert to cytoscape.js json file
    """
    cols_to_show = [c for c in df.header() if c != "_structure"]
    g_dict = {"nodes": [], "edges": [], "columns": cols_to_show}
    for n, attr in df.graph.nodes(data=True):
        mol = attr["elem"]
        svg = SVG(mol)
        svg.screen_size = (100, 100)
        d = {
            "id": n,
            "src": svg.data_url_scheme(),
            "width": svg.screen_size[0],
            "height": svg.screen_size[1],
            "degree": df.graph.degree(n)
        }
        for col in cols_to_show:
            d[col] = df[col][n]
        g_dict["nodes"].append(d)
    for u, v, attr in df.graph.edges(data=True):
        d = {
            "source": g_dict["nodes"][u]["id"],
            "target": g_dict["nodes"][v]["id"],
            "dist": attr["dist"]
        }
        g_dict["edges"].append(d)
    return json.dumps(g_dict)


class GraphWorker(Worker):
    def __init__(self, args, func, args_size, arrs, dfcont, df_id):
        super().__init__(args, func, args_size)
        self.dist_threshold = 0.7
        self.dfcontainer = dfcont
        self.df_id = df_id
        self._graph = nx.Graph()
        for i, _, c in arrs:
            self._graph.add_node(i, elem=c, type="node")

    def on_task_done(self, res):
        u, v, d = res
        if d < self.dist_threshold:
            self._graph.add_edge(u, v, dist=d)

    def on_finish(self):
        self.dfcontainer.container[self.df_id].graph = self._graph


class GenerateGraphHandler(BaseHandler):
    @web.authenticated
    def post(self):
        measure = self.get_argument("measure")
        thld = float(self.get_argument("dist"))
        df_id = self.get_cookie("df")
        mols = self.get_df()["_mol"]
        if measure == "gls":
            diam = int(self.get_argument("diam"))
            tree = int(self.get_argument("tree"))
            skip = int(self.get_argument("skip"))
            arrs, args, alen = csmap_args(mols, diam, tree, skip)
            worker = GraphWorker(args, mp_gls_dist, alen,
                                 arrs, self.dfcont, df_id)
            worker.dist_threshold = thld
            self.wqueue.put(df_id, worker)
        elif measure == "morgan":
            G = nx.Graph()
            for i, mol in enumerate(mols):
                G.add_node(i, elem=mol, type="node")
            for m1, m2 in combinations(enumerate(mols), 2):
                d = round(1 - rdkit.morgan_similarity(m1[1], m2[1]), 2)
                if d < thld:
                    G.add_edge(m1[0], m2[0], dist=d)
            self.dfcont.container[df_id].graph = G
        self.redirect('/')


class GraphUpdateHandler(BaseHandler):
    @web.authenticated
    def get(self):
        df = self.get_df()
        self.write(graph_to_json(df))
