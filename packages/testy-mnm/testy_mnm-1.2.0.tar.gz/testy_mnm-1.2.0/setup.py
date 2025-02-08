from setuptools import setup, find_packages, Extension
from distutils.command.build import build
import os
import shutil
import sys
import numpy as np

testy_c_module = Extension(
    'testy_mnm.core.testy_c_module',
    sources=[
        'testy_mnm/core/src/module.c'
    ],
    include_dirs=[np.get_include()],
)

setup(
    name='testy_mnm',
    version='1.2.0',
    packages=find_packages(),
    ext_modules=[testy_c_module],
)
