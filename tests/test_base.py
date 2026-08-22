"""Behaviour tests for the declarative base and naming convention."""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import NAMING_CONVENTION, Base


def test_naming_convention_covers_all_constraint_kinds() -> None:
    assert set(NAMING_CONVENTION) == {"ix", "uq", "ck", "fk", "pk"}
    assert NAMING_CONVENTION["ix"] == "ix_%(table_name)s_%(column_0_name)s"
    assert NAMING_CONVENTION["uq"] == "uq_%(table_name)s_%(column_0_name)s"
    assert NAMING_CONVENTION["ck"] == "ck_%(table_name)s_%(constraint_name)s"
    assert (
        NAMING_CONVENTION["fk"]
        == "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    )
    assert NAMING_CONVENTION["pk"] == "pk_%(table_name)s"


def test_base_uses_naming_convention() -> None:
    assert Base.metadata.naming_convention == NAMING_CONVENTION


def test_constraint_names_are_generated() -> None:
    class ConventionBase(DeclarativeBase):
        metadata = MetaData(naming_convention=NAMING_CONVENTION)

    class Row(ConventionBase):
        __tablename__ = "rows"
        id: Mapped[int] = mapped_column(primary_key=True)
        code: Mapped[str] = mapped_column(unique=True)

    assert Row.__table__.primary_key.name == "pk_rows"
    constraint_names = {constraint.name for constraint in Row.__table__.constraints}
    assert "uq_rows_code" in constraint_names
