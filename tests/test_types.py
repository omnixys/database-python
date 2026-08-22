"""Behaviour tests for the Uuid7 and UtcDateTime column types."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from database import UtcDateTime, Uuid7, generate_uuid7


def test_generate_uuid7_returns_uuid_version_7() -> None:
    value = generate_uuid7()

    assert isinstance(value, uuid.UUID)
    assert value.version == 7


def test_generate_uuid7_returns_unique_values() -> None:
    assert generate_uuid7() != generate_uuid7()


def test_uuid7_generates_when_bind_value_is_none() -> None:
    generated = Uuid7().process_bind_param(None, None)

    assert isinstance(generated, uuid.UUID)
    assert generated.version == 7


def test_uuid7_passes_bind_value_through() -> None:
    value = uuid.uuid4()

    assert Uuid7().process_bind_param(value, None) is value


def test_uuid7_passes_result_value_through() -> None:
    value = uuid.uuid4()

    assert Uuid7().process_result_value(value, None) is value


def test_uuid7_impl_is_postgres_uuid() -> None:
    from sqlalchemy.dialects.postgresql import UUID

    assert isinstance(Uuid7().impl, UUID)


def test_utcdatetime_passes_naive_result_through() -> None:
    value = datetime(2026, 1, 2, 3, 4, 5)  # noqa: DTZ001

    assert UtcDateTime().process_result_value(value, None) == value


def test_utcdatetime_passes_aware_result_through() -> None:
    value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)

    assert UtcDateTime().process_result_value(value, None) == value


def test_utcdatetime_passes_bind_value_through() -> None:
    value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)

    assert UtcDateTime().process_bind_param(value, None) == value
