# 
# setup.py : pyvoro python interface to voro++
# 
# this extension to voro++ is released under the original modified BSD license
# and constitutes an Extension to the original project.
#
# Copyright (c) Joe Jordan 2012
# contact: <joe.jordan@imperial.ac.uk> or <tehwalrus@h2j9k.org>
#

from distutils.core import setup, Extension
import sys

if sys.platform == 'darwin':
    extra_compile_args=['-arch','arm64e','-arch','x86_64','-arch','arm64']
    extra_link_args=['-arch','arm64e','-arch','x86_64','-arch','arm64']
else:
    extra_compile_args=[]
    extra_link_args=[]

# fall back to provided cpp file if Cython is not found
extensions = [
    Extension("voroplusplus",
              sources=["pyvoro/voroplusplus.cpp",
                       "pyvoro/vpp.cpp",
                       "src/voro++.cc"],
              include_dirs=["src"],
              language="c++",
              extra_compile_args=extra_compile_args,
              extra_link_args=extra_link_args,
              )
]

setup(
    name="pyvoro",
    version="1.3.3",
    description="2D and 3D Voronoi tessellations: a python entry point for the voro++ library.",
    author="Joe Jordan",
    author_email="joe.jordan@imperial.ac.uk",
    url="https://github.com/joe-jordan/pyvoro",
    download_url="https://github.com/joe-jordan/pyvoro/tarball/v1.3.3",
    packages=["pyvoro",],
    package_dir={"pyvoro": "pyvoro"},
    ext_modules=extensions,
    keywords=["geometry", "mathematics", "Voronoi"],
    classifiers=[],
)
