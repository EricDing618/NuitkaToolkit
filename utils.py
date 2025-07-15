import platform
import sys
import os
import json
import subprocess
import re

from packaging import version
from typing import Tuple, Optional
from pathlib import Path

with open("settings.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

COMPAT = {
    ((3,12),None): ((2,3),None),
    ((3,8),(3,11)): ((1,8),None),
    ((3,6),(3,7)): ((1,7),(1,7)),
    ((2,7),(2,7)): ((0,6,19,4),(0,6,19,4))
}
VER_PY = sys.version_info[:2]

def get_os_details() -> Tuple[str, Optional[str], Optional[str]]:
    """返回 (系统类型, 发行版名称, 版本号)"""
    system = platform.system().lower()
    distro_name = None
    distro_version = None

    # Linux发行版精确识别
    if system == "linux":
        try:
            import distro  # pip install distro
            distro_name = distro.id()
            distro_version = distro.version()
        except ImportError:
            # 降级方案：解析/etc/os-release
            try:
                with open("/etc/os-release") as f:
                    os_release = dict(
                        line.strip().split("=", 1)
                        for line in f
                        if "=" in line
                    )
                    distro_name = os_release.get("ID", "").strip('"')
                    distro_version = os_release.get("VERSION_ID", "").strip('"')
            except FileNotFoundError:
                # 针对CentOS/RHEL的备用方案
                try:
                    with open("/etc/redhat-release") as f:
                        release = f.read()
                        if "centos" in release.lower():
                            distro_name = "centos"
                            distro_version = release.split()[3]  # 如"7.9.2009"
                except FileNotFoundError:
                    pass

    # Windows/macOS处理
    elif system == "windows":
        distro_version = platform.win32_ver()[1]  # 如"10.0.19045"
    elif system == "darwin":
        distro_version = platform.mac_ver()[0]  # 如"13.4.1"

    return system, distro_name, distro_version

def is_in_container() -> bool:
    """检查是否运行在容器中"""
    paths = ["/.dockerenv", "/run/.containerenv"]
    return any(os.path.exists(path) for path in paths) or \
           os.environ.get("container") == "docker"

arch = platform.machine()  # x86_64/arm64/aarch64
if arch == "aarch64":
    arch = "arm64"  # 统一命名

def get_nuitka_versions_legacy_pip():
    """通过 pip install 模拟获取版本（兼容旧版 pip）"""
    try:
        result = subprocess.run(
            ["pip", "install", "Nuitka=="],  # 故意不指定版本
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # 从错误信息中提取版本号
        versions = []
        for line in result.stderr.splitlines():
            if "Could not find a version" in line:
                versions_str = re.search(r"\(from versions: (.*?)\)", line).group(1)
                versions = [v.strip() for v in versions_str.split(",")]
                break

        # 过滤预发布版本
        stable_versions = [
            v for v in versions 
            if not version.parse(v).is_prerelease
        ]
        stable_versions.sort(key=lambda x: version.parse(x), reverse=True)
        return stable_versions

    except Exception as e:
        print(f"通过 pip install 模拟获取版本失败: {e}")
        return []