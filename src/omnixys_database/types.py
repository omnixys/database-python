from __future__ import annotations

# ruff: noqa: D100, D101, D102, D103, ANN401, ARG002
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID


def generate_uuid7() -> uuid.UUID:
    return uuid.uuid7()


class Uuid7(TypeDecorator[uuid.UUID]):
    impl = UUID(as_uuid=True)
    cache_ok = True

    def process_bind_param(self, value: uuid.UUID | None, dialect: Any) -> uuid.UUID | None:
        return value if value is not None else generate_uuid7()

    def process_result_value(self, value: uuid.UUID | None, dialect: Any) -> uuid.UUID | None:
        return value


class UtcDateTime(TypeDecorator[datetime]):
    impl = DateTime(timezone=True)
    cache_ok = True
    localize = True

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        return value

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None and value.tzinfo is None:
            return value.replace(tzinfo=None)
        return value
