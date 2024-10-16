"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['Image Resizer.py']
DATA_FILES = ['dnd.png']
OPTIONS = {'iconfile': '/Users/bryan-plaid/repos/py-images/ir.icns', 'packages': 'setuptools'}

setup(
    name="Image Resizer",
    version="1.0.0",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
