# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['path\\to\\your\\EatWhat\\main.py'],
    pathex=['path\\to\\your\\EatWhat'],
    binaries=[],
    datas=[
        ("path\\to\\your\\EatWhat\\Crawler\\*", 'Crawler'),
        ("path\\to\\your\\EatWhat\\UI\\*", 'UI'),
        ("path\\to\\your\\EatWhat\\UI\\img\\*", 'UI/img'),
        ("path\\to\\your\\EatWhat\\UI\\img\\icon\\*", 'UI/img/icon'),
        ('path\\to\\your\\playwright\\*', 'playwright'), 
        # Please leave only two folder ".links" and "chromium-1117" in "playwright\driver\package\.local-browsers\",
        # Remaining other folders in "playwright\driver\package\.local-browsers\" must be deleted manually.
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0, 
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EatWhat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX to compress.
    upx_exclude=[], 
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='path\\to\\your\\EatWhat\\UI\\img\\icon\\ICON_eatwhat.ico',
)
