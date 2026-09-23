from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel

from domain import AccessDenied, AuthContext, RevenueService


class InMemoryRevenueRepository:
    """Synthetic repository used only by this public example."""

    def __init__(self) -> None:
        self._totals: dict[UUID, Decimal] = {}

    def set_total(self, company_id: UUID, total: Decimal) -> None:
        self._totals[company_id] = total

    def total_for_company(self, company_id: UUID) -> Decimal:
        return self._totals.get(company_id, Decimal("0.00"))


class RevenueResponse(BaseModel):
    company_id: UUID
    total: Decimal


repository = InMemoryRevenueRepository()
service = RevenueService(repository)
app = FastAPI(title="ALRYA public architecture sample")


def demo_context(
    x_demo_user_id: UUID = Header(alias="X-Demo-User-ID"),
    x_demo_company_id: UUID = Header(alias="X-Demo-Company-ID"),
    x_demo_permissions: str = Header(
        default="revenue:read",
        alias="X-Demo-Permissions",
    ),
) -> AuthContext:
    """
    Self-contained demo dependency.

    A real application should derive this context from authenticated identity
    and server-side authorization. Client-provided demo headers are not a
    production authentication mechanism.
    """
    permissions = frozenset(
        item.strip()
        for item in x_demo_permissions.split(",")
        if item.strip()
    )
    return AuthContext(
        user_id=x_demo_user_id,
        company_id=x_demo_company_id,
        permissions=permissions,
    )


@app.get(
    "/demo/companies/{company_id}/revenue",
    response_model=RevenueResponse,
)
def get_revenue(
    company_id: UUID,
    context: AuthContext = Depends(demo_context),
) -> RevenueResponse:
    try:
        summary = service.summary(
            context=context,
            requested_company_id=company_id,
        )
    except AccessDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return RevenueResponse(
        company_id=summary.company_id,
        total=summary.total,
    )
