# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# collect vosk's native DLLs explicitly
vosk_binaries = collect_dynamic_libs('vosk')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=vosk_binaries,
    datas=[
        # Vosk model folder — required for speech recognition
        ('vosk-model-small-en-us-0.15', 'vosk-model-small-en-us-0.15'),
        # feature modules — required for auto-discovery
        ('features', 'features'),
        # core modules
        ('core', 'core'),
    ],
    hiddenimports=[
        # dynamic imports not detected by static analysis
        'features.general',
        'features.dev_tools',
        'core.registry',
        'core.listener',
        'core.speaker',
        'core.logger',
        'core.nlu.normalizer',
        'core.nlu.classifier',
    ],
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
    name='jack',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
