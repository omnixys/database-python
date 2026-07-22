"""Smoke test - verifies omnixys-database can be imported."""

from __future__ import annotations

import importlib
from importlib.metadata import version as pkg_version


def test_package_importable() -> None:
    mod = importlib.import_module("database")
    assert hasattr(mod, "__version__")
    assert mod.__version__ == pkg_version("omnixys-database")


def test_public_api() -> None:
    from database import base, session, types

    assert base is not None
    assert session is not None
    assert types is not None
