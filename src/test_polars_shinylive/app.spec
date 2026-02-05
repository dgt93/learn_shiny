# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for the Shiny dashboard app."""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all submodules for complex packages
hidden_imports = (
    collect_submodules("shiny")
    + collect_submodules("htmltools")
    + collect_submodules("starlette")
    + collect_submodules("uvicorn")
    + collect_submodules("anyio")
    + collect_submodules("plotly")
    + collect_submodules("faicons")
    + collect_submodules("shinywidgets")
    + collect_submodules("webview")
    + ["h11", "websockets", "websockets.legacy", "websockets.legacy.server"]
)

# Collect data files (templates, static assets, etc.)
datas = (
    [
        ("app.py", "app"),
        ("shared.py", "app"),
        ("penguins.csv", "app"),
        ("styles.css", "app"),
    ]
    + collect_data_files("shiny")
    + collect_data_files("htmltools")
    + collect_data_files("faicons")
    + collect_data_files("shinywidgets")
)

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PenguinsDashboard",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hidden - using pywebview for native window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
