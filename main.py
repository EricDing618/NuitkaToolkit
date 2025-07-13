__version__ = "0.1.0"

from utils import *
PIPATH = get_pip_path_via_import()

try:
    from nuitka import Version as nkver
    VER_NK = nkver.getNuitkaVersionTuple()
    def compat():
        for py, nk in COMPAT:
            if (VER_PY >= py[0] and (VER_PY <= py[1] or py[1] is None)) and ((VER_NK >= nk[0] or nk[0] is None) and (VER_NK <= nk[1] or nk[1] is None)):
                return True
        return False
except ImportError:
    print("检测到未安装Nuitka，正在尝试安装...")
    os.system()

class Arg:
    def __init__(self, name, have_value=False, value=None):
        self.name = name
        self.have_value = have_value
        self.value = value

class NuitkaToolkitCLI:
    def __init__(self):
        self.last_cli = None
        self.args = [Arg('nuitka')]

if __name__ == '__main__':
    NuitkaToolkitCLI()