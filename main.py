__version__ = "0.1.0"

from utils import *

def best_versions():
    for py, nk in COMPAT.items():
        print(py, nk)
        if ((VER_PY >= py[0] or py[0] is None) and (VER_PY <= py[1] or py[1] is None)):
            return nk
    return None
little, large = best_versions()
try:
    from nuitka import Version as nkver
except ImportError:
    print("检测到未安装Nuitka，正在尝试安装...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"nuitka=={little}"])
    except:
        print("安装Nuitka失败，请手动安装Nuitka")
        sys.exit(1)
    else:
        from nuitka import Version as nkver
        print("安装Nuitka成功")
VER_NK = nkver.getNuitkaVersionTuple()[:3]
print(f"当前Python版本: {VER_PY}")
print(f"当前Nuitka版本: {VER_NK}")
def is_compatible():
    if best_versions() is not None:
        if (little is None or VER_NK >= little) and (large is None or VER_NK <= large):
            return True
    return False
if not is_compatible():
    print(f"当前Python版本与Nuitka版本不兼容，正在尝试安装nuitka=={little}")
else:
    print("当前Python版本与Nuitka版本兼容")


class Arg:
    def __init__(self, name, value=None, have_value=False):
        self.name = name
        self.have_value = have_value
        self.value = value
        if have_value:
            self.cmd = f"--{name}={value}"
        else:
            self.cmd = f"--{name}"

class CLI:
    def __init__(self, all:dict[str, list[str,list]]):
        self.all = all
        self.page = 0
    def show_next(self, ask=''):
        ...

class NuitkaToolkit:
    def __init__(self):
        self.last_cli = None
        self.args = [Arg('nuitka')]
        self.cli = CLI({
            0: []
        })
    

if __name__ == '__main__':
    NuitkaToolkit()