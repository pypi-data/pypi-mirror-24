
import glob
import os.path
import sqlite3
import sys

alias_dir_path = os.path.join(os.path.dirname(__file__), "../aliases/")
files = glob.glob(os.path.join(alias_dir_path, "*.tsv"))

records = []

for file_ in files:
    with open(file_) as f:
        for line in f:
            try:
                a, b = line.split("\t")
            except ValueError:
                sys.exit("Error: incorrect format file {}".format(file_))
            records.append((a, b))

conn = sqlite3.connect(os.path.join(alias_dir_path, "aliases.sqlite3"))
c = conn.cursor()
c.execute("CREATE TABLE aliases (id text, alias text)")
c.executemany("INSERT INTO aliases VALUES (?, ?)", records)
conn.commit()
conn.close()
