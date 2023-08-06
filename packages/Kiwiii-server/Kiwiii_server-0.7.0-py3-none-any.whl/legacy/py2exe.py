
from distutils.core import setup
from glob import glob
import sys
import py2exe

sys.path.append("C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC \
    \\redist\\x86\\Microsoft.VC90.CRT")

option = {
    "compressed": 1,
    "optimize": 2,
    "bundle_files": 3,
    "includes": ["py4j.java_collections"]
}

setup(
    options={"py2exe": option},
    windows=[{"script": "gui_main.py"}],
    data_files=[
        ("java", ["./lib/cheddar_java.jar", "./lib/genedataclient.properties",
         "./lib/genedataclientpolicy.txt"]),
        ("sqlite", ["./sqlite/chemlib.sqlite3"]),
        ("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\Microsoft Visual \
        Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))
    ]
)
