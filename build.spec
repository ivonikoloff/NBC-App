# build.spec — NBC Association Ultimate Hybrid
# Подготвено от ChatGPT x Ивайло

import os
import hashlib
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# -----------------------------
# НАСТРОЙКИ
# -----------------------------
app_name = "NBC_Association"
version = "1.0.0"
entry_script = "app.py"
icon_path = "static/logo.ico"

# -----------------------------
# Събиране на всички модули
# -----------------------------
hiddenimports = collect_submodules("reportlab") + collect_submodules("PyQt6")

a = Analysis(
    [entry_script],
    pathex=["."],
    binaries=[],
    datas=[
        ("static", "static"),
        ("reports", "reports"),
        ("data.json", "."),
    ],
    hiddenimports=hiddenimports,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # без конзола
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
