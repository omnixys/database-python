# omnixys-database

Omnixys shared database package with SQLAlchemy async support.

## Installation

```bash
pip install omnixys-database
```

## Features

- Async SQLAlchemy session management
- PostgreSQL support via asyncpg
- Base models and types (UtcDateTime, Uuid7)
- Pagination utilities

## Usage

```python
from omnixys_database import Base, DatabaseSessionManager, Page, UtcDateTime, Uuid7
```

## License

GPL-3.0-or-later
