"""Smoke test - verifies omnixys-database can be imported."""

from __future__ import annotations

import importlib
from importlib.metadata import version as pkg_version

import database
from database import (
    NAMING_CONVENTION,
    Base,
    DatabaseSessionManager,
    Page,
    UtcDateTime,
    Uuid7,
    generate_uuid7,
)


def test_package_importable() -> None:
    mod = importlib.import_module("database")
    assert mod is not None


def test_package_version() -> None:
    assert pkg_version("omnixys-database")


def test_submodules_available() -> None:
    assert database.base is not None
    assert database.page is not None
    assert database.session is not None
    assert database.types is not None


def test_public_exports() -> None:
    assert Base is not None
    assert DatabaseSessionManager is not None
    assert NAMING_CONVENTION is not None
    assert Page is not None
    assert UtcDateTime is not None
    assert Uuid7 is not None
    assert generate_uuid7 is not None
