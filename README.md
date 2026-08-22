# omnixys-database

Async SQLAlchemy toolkit for Omnixys services: session management, declarative
base models, pagination, and shared column types, built on SQLAlchemy 2.x with
`asyncpg`.

## Installation

```bash
pip install omnixys-database
```

## Features

- **DatabaseSessionManager** — async engine + session factory with lifecycle
  management: `session_scope()` (commit-on-success, rollback+re-raise on error),
  `create_session()`, `close()`, and `async with` support.
- **Base & naming convention** — a declarative base whose metadata applies a
  consistent naming convention (`pk_`, `fk_`, `uq_`, `ix_`, `ck_`) to all
  generated constraints.
- **Uuid7** — PostgreSQL `UUID` column type that generates a v7 UUID for new
  rows when no value is provided.
- **UtcDateTime** — timezone-aware `DateTime` column type.
- **Page** — frozen pagination value object with computed
  `total_pages`/`has_next`/`has_previous`.

## Quick start

```python
import asyncio

from database import DatabaseSessionManager

manager = DatabaseSessionManager(
    "postgresql+asyncpg://omnixys:omnixys@localhost:5432/omnixys",
    echo=False,
    pool_size=10,
    max_overflow=20,
    use_pool=True,
)

async def main() -> None:
    async with manager.session_scope() as session:
        # the transaction is committed when the block exits normally
        # and rolled back when an exception propagates
        ...

    async with manager:
        ...  # manager.close() runs on exit

asyncio.run(main())
```

`session_scope` closes the session in `finally` in all cases. Pass
`use_pool=False` to use a `NullPool` (e.g. for short-lived workers) instead of
the default `AsyncAdaptedQueuePool`.

## Base models

```python
import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database import Base, UtcDateTime, Uuid7
from database.types import generate_uuid7

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid7(), primary_key=True, default=generate_uuid7)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime(), nullable=False)
```

Constraints on models inheriting from `Base` get conventional names
automatically (e.g. a unique column `email` produces `uq_accounts_email`).

## Column types

### Uuid7

```python
import uuid

from sqlalchemy.orm import Mapped, mapped_column

from database import Uuid7
from database.types import generate_uuid7

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid7(), primary_key=True, default=generate_uuid7)
```

PostgreSQL `UUID` column. When the bound value is `None`, a v7 UUID is generated
(v7 is sortable by time, making it suitable for primary keys in large tables).
Existing values pass through unchanged.

### UtcDateTime

```python
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database import UtcDateTime

class Account(Base):
    __tablename__ = "accounts"

    created_at: Mapped[datetime] = mapped_column(UtcDateTime(), nullable=False)
```

Timezone-aware `DateTime` column type; values pass through unmodified.

## Pagination

```python
from database import Page

page = Page(items=[...], total=137, page=2, size=25)

page.total_pages    # 6 (ceil(total / size))
page.has_next       # True
page.has_previous   # True
```

`total_pages` is `ceil(total / size)` (`0` when `size == 0`),
`has_next`/`has_previous` derive from the current page index. `Page` is a frozen
dataclass and compares by value.

## Development

```bash
uv sync
uv run pytest -q
uv run ruff check .
uv run mypy src/
```

## License

GPL-3.0-or-later
