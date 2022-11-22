from setuptools import Extension, setup
from Cython.Build import cythonize

sourcefiles = ['functions.pyx', 'c_astrom2.c']

extensions = [Extension("functions", sourcefiles)]

setup(
    name="functions", ext_modules=cythonize(extensions)
)


