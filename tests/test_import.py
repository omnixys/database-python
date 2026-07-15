"""Smoke test - verifies omnixys-database can be imported."""

from __future__ import annotations

import importlib



def test_package_importable() -> None:
    mod = importlib.import_module("omnixys_database")
    assert hasattr(mod, "__version__")
    assert mod.__version__ == "1.0.0"


def test_public_api() -> None:
    from omnixys_database import base, session, types

    assert base is not None
    assert session is not None
    assert types is not None
