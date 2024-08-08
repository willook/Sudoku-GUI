from setuptools import setup, find_packages

setup(
    name="sudoku-gui",
    version="1.0",
    packages=find_packages(include=["sudoku", "sudoku.*"]),
    description="A Sudoku GUI application",
    author="willook",
    author_email="your@email.com",
    install_requires=[
        "pygame",
        "numpy",
    ],
)
