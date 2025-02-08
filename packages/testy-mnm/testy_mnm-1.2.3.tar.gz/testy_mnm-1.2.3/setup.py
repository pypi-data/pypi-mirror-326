from setuptools import setup, find_packages, Extension
from distutils.command.build import build
import os
import shutil
import sys
import numpy as np

# def find_all_c_files(directory):
#     c_files = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.c'):
#                 dir = os.path.join(root, file)
#                 dir = dir.replace('\\', '/')
#                 c_files.append(dir)

#     return c_files

testy_c_module = Extension(
    'testy_mnm.core.testy_c_module',
    sources=['testy_mnm/core/src/module.c', 'testy_mnm/core/src/src_of_src/head.c'],
    include_dirs=[np.get_include()],
)

setup(
    name='testy_mnm',
    version='1.2.3',
    packages=find_packages(),
    ext_modules=[testy_c_module],
)
