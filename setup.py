import sys
from cx_Freeze import setup, Executable

nom_application: str = "AppUtilitaire"
version: str = "0.1"
repertoire_sortie: str = "build\\" + nom_application + "_v" + version

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = nom_application,
    version = version,
    description = "Sample cx_Freeze Tkinter script",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base = base)])