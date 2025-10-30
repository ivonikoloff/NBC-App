from setuptools import setup

APP = ['app.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6', 'pandas', 'reportlab', 'openpyxl', 'pytesseract', 'Pillow'],
    'includes': ['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    'resources': [],
    'plist': {
        'CFBundleName': 'NBC Member Manager',
        'CFBundleDisplayName': 'NBC Member Manager',
        'CFBundleIdentifier': 'org.nbc.membermanager',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
