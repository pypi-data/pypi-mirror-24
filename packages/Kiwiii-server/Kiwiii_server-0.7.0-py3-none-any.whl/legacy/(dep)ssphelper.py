
import re
import copy
from urllib.parse import parse_qs


def parse_query(query):
    results = {}
    # Parse http query
    q = parse_qs(query)
    parsed = {}
    for k, v in q.items():
        ksps = filter(None, re.split('\[(\w+)\]', k))
        gp = None
        last = None
        parent = parsed
        for ksp in ksps:
            if ksp not in parent:
                parent[ksp] = {}
            gp = parent
            last = ksp
            parent = parent[ksp]
        gp[last] = v[0]

    if "start" in parsed and parsed["length"] != -1:
        results["limit"] = (parsed["start"], parsed["length"])

    if "order" in parsed:
        od = {}
        for k in parsed["order"].keys():
            idx = parsed["order"][k]["column"]
            col = parsed["columns"][idx]
            if col["orderable"] == "true":
                if parsed["order"][k]["dir"] == "asc":
                    od[idx] = True
                else:
                    od[idx] = False
        results["order"] = od

    sh = {}
    for k in parsed["columns"].keys():
        col = parsed["columns"][k]
        if col["searchable"] == "true":
            if "value" in col["search"]:
                sh[k] = parsed["columns"][k]["search"]["value"]
    results["filter"] = sh

    results["draw"] = parsed["draw"]
    print(results)
    return results


def update_table(query, df):
    row_count = df.row_count()
    filtered_count = df.row_count()
    cdf = copy.copy(df)
    if query["order"]:
        for k, v in query["order"].items():
            cdf.df = cdf.df.sort(columns=cdf.df.columns[k],  ascending=v)

    data = []
    for i, row in cdf.df.iterrows():
        data.append(row.tolist())
    results = {
        "draw": int(query["draw"]),
        "recordsTotal": row_count,
        "recordsFiltered": filtered_count,
        "data": data
    }
    return results
