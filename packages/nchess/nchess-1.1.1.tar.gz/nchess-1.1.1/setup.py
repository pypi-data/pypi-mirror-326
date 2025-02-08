import os
import numpy
from setuptools import setup, find_packages, Extension

this_dir = '.'
core_dir = os.path.join(this_dir, "nchess/core")
build_path = os.path.join(core_dir, "build")

def find_c_files(directory):
    c_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.c')]
    return c_files

nchess_module = Extension(
    'nchess.core.nchess_core',
    sources=[
        *find_c_files(os.path.join(core_dir, 'src')),
        *find_c_files(os.path.join(core_dir, 'src/nchess')),
    ],
    include_dirs=[
        "nchess/core/src",
        "nchess/core/src/nchess",
        numpy.get_include(),
    ],
)

setup(
    name='nchess',
    version='1.1.1',
    ext_modules=[
            nchess_module
        ],
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0', "wheel", "setuptools>=42"
    ],
)
