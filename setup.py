from setuptools import setup
from Cython.Build import cythonize

# Used for compiling Cython code
setup(
    ext_modules=cythonize("mazeGenerator/controllers/boardHelper.pyx")
)
