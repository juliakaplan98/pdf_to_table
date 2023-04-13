import os
from setuptools import setup, find_packages

exec(open("pdfmanipulator/version.py").read())

setup(
    name="pdfmanipulator",
    version=__version__,
    description="Extractor tables from PDF",
    url="https://github.com/juliakaplan98/pdf_to_table",
    author="Julia Kaplan",
    author_email="juliakaplan98@outlook.com",
    license="BSD 3-Clause License",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Anybody",
        "Topic :: PDF",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        "PyPDF4",
        "tabula",
        "pandas",
        "numpy",
    ],
    extras_require={
        ':python_version>="3.11"': ["configparser", "pyqt6"],
    },
    package_data={
        "pdfmanipulator": [
            "volumerender/kernels/*",
            "gui/shaders/*",
            "gui/images/*",
            "colormaps/*",
            "data/*",
            "lib/*",
        ]
    },
    entry_points={
        "pdfmanipulator": [
            "pdfmanipulator = pdfmanipulator.pdfmanipulator.index:main"
        ]
    },
)
