import os
import numpy
from setuptools import setup, find_packages, Extension

this_dir = '.'
python_src = os.path.join(this_dir, "nchess/core/src")
c_src = os.path.join(this_dir, "nchess/core/src/nchess")

nchess_module = Extension(
    'nchess.core.nchess_core',
    sources=[
        *[os.path.join(python_src, f) for f in os.listdir(python_src) if f.endswith('.c')],
        *[os.path.join(c_src, f) for f in os.listdir(c_src) if f.endswith('.c')],
    ],
    include_dirs=[
        python_src,
        c_src,
        numpy.get_include(),
    ],
)

setup(
    name='nchess',
    version='1.1.3',
    ext_modules=[
            nchess_module
        ],
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0', "wheel", "setuptools>=42"
    ],
    author='MNMoslem',
    author_email='normoslem256@gmail.com',
    description='chess library written in c',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MNourMoslem/NChess',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    license=open('LICENSE').read(),
)
