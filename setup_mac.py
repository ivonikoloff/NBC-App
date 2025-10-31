from setuptools import setup

APP = ['app.py']
DATA_FILES = ['static', 'reports', 'data.json']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['reportlab', 'PyQt6', 'pandas', 'sqlite3'],
    'iconfile': 'static/logo.icns',
    'plist': {
        'CFBundleName': 'NBC Association',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'org.nbc.association',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
