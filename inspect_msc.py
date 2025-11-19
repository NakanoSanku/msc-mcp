import inspect
from msc.adbcap import ADBCap
from msc.droidcast import DroidCast
from msc.minicap import MiniCap
from msc.mumu import MuMuCap

def print_methods(cls, name):
    print(f"--- {name} Methods ---")
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith("_"):
            print(f"{name}: {inspect.signature(func)}")
    print("-----------------------")

print_methods(ADBCap, "ADBCap")
print_methods(DroidCast, "DroidCast")
print_methods(MiniCap, "MiniCap")
print_methods(MuMuCap, "MuMuCap")
