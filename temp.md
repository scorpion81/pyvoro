# Modernisierung von `pyvoro` auf scikit-build-core + CMake

Dieses Dokument zeigt eine vollständige 1:1-Migration des klassischen `distutils`-basierten `pyvoro` Repos auf einen modernen Build-Stack mit:

* CMake
* scikit-build-core
* PEP517 / pyproject.toml
* Python wheel support
* macOS universal2 support
* Linux / Windows kompatible native builds

---

# Zielstruktur

```text
pyvoro/
├── pyproject.toml
├── CMakeLists.txt
├── README.md
├── LICENSE
├── src/
│   └── voro++.cc
├── pyvoro/
│   ├── __init__.py
│   ├── voroplusplus.cpp
│   └── vpp.cpp
└── tests/
```

---

# 1. pyproject.toml

Die wichtigste Datei im modernen Python Build-System.

```toml
[build-system]
requires = [
    "scikit-build-core>=0.9",
    "cmake>=3.18",
    "ninja",
    "setuptools",
    "wheel"
]
build-backend = "scikit_build_core.build"

[project]
name = "pyvoro"
version = "1.3.3"
description = "2D and 3D Voronoi tessellations: Python bindings for voro++"
readme = "README.md"
authors = [
    { name = "Joe Jordan", email = "joe.jordan@imperial.ac.uk" }
]
license = { text = "BSD" }
requires-python = ">=3.8"
keywords = ["geometry", "Voronoi", "mathematics"]
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: C++",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows"
]

[tool.scikit-build]
wheel.packages = ["pyvoro"]

[tool.scikit-build.cmake]
minimum-version = "3.18"

[tool.scikit-build.cmake.define]
CMAKE_CXX_STANDARD = "17"
```

---

# 2. CMakeLists.txt

Dies ersetzt praktisch den gesamten nativen Build-Teil aus setup.py.

```cmake
cmake_minimum_required(VERSION 3.18)

project(pyvoro LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

add_library(voroplusplus MODULE
    pyvoro/voroplusplus.cpp
    pyvoro/vpp.cpp
    src/voro++.cc
)

# Include directories

target_include_directories(voroplusplus PRIVATE
    src
    ${Python3_INCLUDE_DIRS}
)

# Windows fixes
if(WIN32)
    target_compile_definitions(voroplusplus PRIVATE NOMINMAX)
endif()

# Python extension naming
set_target_properties(voroplusplus PROPERTIES
    PREFIX ""
    OUTPUT_NAME "voroplusplus"
    SUFFIX "${Python3_EXTENSION_MODULE_SUFFIX}"
)

# Install into wheel
install(TARGETS voroplusplus
        LIBRARY DESTINATION pyvoro
        RUNTIME DESTINATION pyvoro)
```

---

# 3. pyvoro/**init**.py

```python
from .voroplusplus import *
```

---

# 4. Entfernen alter Dateien

Diese Dateien werden NICHT mehr benötigt:

```text
setup.py
MANIFEST.in
setup.cfg
```

Optional kannst du ein minimales compatibility setup.py behalten:

```python
from setuptools import setup
setup()
```

Aber empfohlen ist:

→ setup.py komplett löschen.

---

# 5. Builden des Projekts

## Build Dependencies installieren

```bash
python -m pip install build
```

---

## Wheel bauen

```bash
python -m build --wheel
```

Output:

```text
dist/pyvoro-1.3.3-....whl
```

---

# 6. macOS universal2 Builds

## Empfohlenes Setup

```bash
export MACOSX_DEPLOYMENT_TARGET=12.0
export CMAKE_OSX_ARCHITECTURES="arm64;x86_64"
```

Dann:

```bash
python -m build --wheel
```

---

# 7. Linux Builds

Einfach:

```bash
python -m build --wheel
```

Für portable wheels später:

* cibuildwheel
* manylinux

---

# 8. Windows Builds

## MSVC Build Tools installieren

```powershell
winget install Microsoft.VisualStudio.2022.BuildTools
```

Dann:

```powershell
python -m build --wheel
```

---

# 9. Vorteile gegenüber distutils

## Vorher

* manuelle -arch flags
* fragile macOS detection
* distutils deprecated
* kein echtes wheel backend
* schwierige CI integration

---

## Nachher

* moderner PEP517 build stack
* native CMake integration
* sauberer universal2 support
* Windows/Linux/macOS identisch
* reproduzierbare builds
* CI-ready

---

# 10. Empfohlene Zusatztools

## Für CI und Release Builds

Installieren:

```bash
python -m pip install cibuildwheel
```

Damit lassen sich automatisch bauen:

* macOS x86_64
* macOS arm64
* universal2
* Linux manylinux
* Windows wheels

---

# 11. Empfohlene GitHub Actions Pipeline

Später empfohlen:

```yaml
name: wheels

on:
  push:
  pull_request:

jobs:
  build:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - run: python -m pip install build

      - run: python -m build --wheel
```

---

# 12. Empfehlung speziell für pyvoro

Das Projekt eignet sich hervorragend für:

* scikit-build-core
* pybind11 Migration
* modern C++ packaging
* automated wheel distribution

Später könnte zusätzlich migriert werden auf:

* pybind11
* nanobind
* cibuildwheel
* GitHub Releases automation

---

# 13. Minimaler Migrationspfad

Wenn du möglichst wenig ändern willst:

1. setup.py löschen
2. pyproject.toml hinzufügen
3. CMakeLists.txt hinzufügen
4. build via `python -m build`

Der bestehende native C++ Code kann unverändert bleiben.
