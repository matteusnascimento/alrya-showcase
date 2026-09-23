from decimal import Decimal
from uuid import UUID

import pytest

from domain import AccessDenied, AuthContext, RevenueService


COMPANY_A = UUID("11111111-1111-1111-1111-111111111111")
COMPANY_B = UUID("22222222-2222-2222-2222-222222222222")
USER = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


class FakeRevenueRepository:
    def __init__(self) -> None:
        self.calls: list[UUID] = []

    def total_for_company(self, company_id: UUID) -> Decimal:
        self.calls.append(company_id)
        return Decimal("1234.50")


def context(
    *,
    company_id: UUID = COMPANY_A,
    permissions: frozenset[str] = frozenset({"revenue:read"}),
) -> AuthContext:
    return AuthContext(
        user_id=USER,
        company_id=company_id,
        permissions=permissions,
    )


def test_returns_revenue_for_the_active_company() -> None:
    repository = FakeRevenueRepository()
    service = RevenueService(repository)

    result = service.summary(
        context=context(),
        requested_company_id=COMPANY_A,
    )

    assert result.company_id == COMPANY_A
    assert result.total == Decimal("1234.50")
    assert repository.calls == [COMPANY_A]


def test_blocks_cross_company_access_before_querying_repository() -> None:
    repository = FakeRevenueRepository()
    service = RevenueService(repository)

    with pytest.raises(AccessDenied, match="Cross-company"):
        service.summary(
            context=context(company_id=COMPANY_A),
            requested_company_id=COMPANY_B,
        )

    assert repository.calls == []


def test_requires_module_permission() -> None:
    repository = FakeRevenueRepository()
    service = RevenueService(repository)

    with pytest.raises(AccessDenied, match="revenue:read"):
        service.summary(
            context=context(permissions=frozenset()),
            requested_company_id=COMPANY_A,
        )

    assert repository.calls == []
