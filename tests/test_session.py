"""Behaviour tests for the DatabaseSessionManager."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

from database import DatabaseSessionManager

URL = "postgresql+asyncpg://localhost:5432/omnixys"


class FakeSession:
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False
        self.closed = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True

    async def close(self) -> None:
        self.closed = True

    async def __aenter__(self) -> FakeSession:
        return self

    async def __aexit__(self, *args: object) -> None:
        return None


class FakeSessionFactory:
    def __init__(self) -> None:
        self.sessions: list[FakeSession] = []

    def __call__(self) -> FakeSession:
        session = FakeSession()
        self.sessions.append(session)
        return session


def make_manager(**kwargs: object) -> DatabaseSessionManager:
    return DatabaseSessionManager(URL, **kwargs)


def test_default_pool_is_async_queue_pool() -> None:
    assert isinstance(make_manager().engine.sync_engine.pool, AsyncAdaptedQueuePool)


def test_null_pool_when_pooling_disabled() -> None:
    manager = make_manager(use_pool=False)

    assert isinstance(manager.engine.sync_engine.pool, NullPool)


def test_echo_is_propagated() -> None:
    assert make_manager(echo=True).engine.echo is True
    assert make_manager(echo=False).engine.echo is False


def test_session_factory_is_async_sessionmaker() -> None:
    assert isinstance(make_manager().session_factory, async_sessionmaker)


async def test_create_session_returns_async_session() -> None:
    session = await make_manager().create_session()

    assert isinstance(session, AsyncSession)
    await session.close()


async def test_session_scope_commits_on_success(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = make_manager()
    factory = FakeSessionFactory()
    monkeypatch.setattr(manager, "_session_factory", factory)

    async with manager.session_scope() as session:
        assert session is factory.sessions[0]

    session = factory.sessions[0]
    assert session.committed is True
    assert session.rolled_back is False
    assert session.closed is True


async def test_session_scope_rolls_back_and_reraises_on_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manager = make_manager()
    factory = FakeSessionFactory()
    monkeypatch.setattr(manager, "_session_factory", factory)

    with pytest.raises(RuntimeError, match="boom"):
        async with manager.session_scope():
            raise RuntimeError("boom")

    session = factory.sessions[0]
    assert session.committed is False
    assert session.rolled_back is True
    assert session.closed is True


async def test_close_disposes_engine_idempotently() -> None:
    manager = make_manager()

    await manager.close()
    await manager.close()


async def test_async_context_manager_closes(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = make_manager()
    closed = False

    async def fake_close() -> None:
        nonlocal closed
        closed = True

    monkeypatch.setattr(manager, "close", fake_close)

    async with manager as entered:
        assert entered is manager

    assert closed is True
