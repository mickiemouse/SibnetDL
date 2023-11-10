import sys
from cx_Freeze import setup, Executable

# Uygulama adı ve ikonu
application_title = "SibnetDL"
base = None

if sys.platform == "win32":
    base = "Win32GUI"  # GUI uygulaması için gerekli

# Executable ile ana betiği ve exe dosyasının adı tanımlanır
exe = Executable(script="sibnetDLGUI.py", base=base, icon="icon.png")

# setup() fonksiyonu ile proje ayarları tanımlanır
setup(
    name="SibnetDL",
    version="1.0",
    description="SibnetDL Uygulaması",
    options={"build_exe": {
        "include_files": [
            ".gitignore",
            "app.js",
            "getEpis.py",
            "LICENSE",
            "node_modules",
            "package-lock.json",
            "package.json",
            "README.md",
            "setup.py",
            "SibnetDL.png",
            "icon.png"
        ]
    }},
    executables=[exe]
)
