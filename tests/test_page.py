"""Behaviour tests for the Page pagination value object."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from database import Page


def test_page_exposes_inputs() -> None:
    page = Page(items=["a", "b", "c"], total=7, page=0, size=3)

    assert page.items == ["a", "b", "c"]
    assert page.total == 7
    assert page.page == 0
    assert page.size == 3


def test_total_pages_is_ceil_division() -> None:
    assert Page(items=[], total=7, page=0, size=3).total_pages == 3
    assert Page(items=[], total=6, page=0, size=3).total_pages == 2
    assert Page(items=[], total=0, page=0, size=3).total_pages == 0
    assert Page(items=[], total=1, page=0, size=3).total_pages == 1


def test_zero_size_yields_zero_total_pages() -> None:
    page = Page(items=[], total=5, page=0, size=0)

    assert page.total_pages == 0


def test_first_page_has_previous_false() -> None:
    page = Page(items=[], total=9, page=0, size=3)

    assert page.has_previous is False
    assert page.has_next is True


def test_middle_page_has_both() -> None:
    page = Page(items=[], total=9, page=1, size=3)

    assert page.has_previous is True
    assert page.has_next is True


def test_last_page_has_next_false() -> None:
    page = Page(items=[], total=9, page=2, size=3)

    assert page.has_previous is True
    assert page.has_next is False


def test_exact_multiple_last_page() -> None:
    page = Page(items=[], total=9, page=2, size=3)

    assert page.page + 1 == page.total_pages
    assert page.has_next is False


def test_page_is_frozen() -> None:
    page = Page(items=[], total=1, page=0, size=1)

    with pytest.raises(FrozenInstanceError):
        page.total = 2


def test_page_is_equal_by_value() -> None:
    assert Page(items=[1], total=1, page=0, size=1) == Page(items=[1], total=1, page=0, size=1)
    assert Page(items=[1], total=1, page=0, size=1) != Page(items=[2], total=1, page=0, size=1)
