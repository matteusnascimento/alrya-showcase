from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID


class AccessDenied(Exception):
    """Raised when a user tries to access a tenant or capability they do not own."""


@dataclass(frozen=True)
class AuthContext:
    user_id: UUID
    company_id: UUID
    permissions: frozenset[str]


@dataclass(frozen=True)
class RevenueSummary:
    company_id: UUID
    total: Decimal


class RevenueRepository(Protocol):
    def total_for_company(self, company_id: UUID) -> Decimal:
        """Return revenue scoped to exactly one company."""


class RevenueService:
    def __init__(self, repository: RevenueRepository) -> None:
        self._repository = repository

    def summary(
        self,
        *,
        context: AuthContext,
        requested_company_id: UUID,
    ) -> RevenueSummary:
        self._require_same_company(context, requested_company_id)
        self._require_permission(context, "revenue:read")

        return RevenueSummary(
            company_id=requested_company_id,
            total=self._repository.total_for_company(requested_company_id),
        )

    @staticmethod
    def _require_same_company(
        context: AuthContext,
        requested_company_id: UUID,
    ) -> None:
        if context.company_id != requested_company_id:
            raise AccessDenied("Cross-company access is not allowed.")

    @staticmethod
    def _require_permission(context: AuthContext, permission: str) -> None:
        if permission not in context.permissions:
            raise AccessDenied(f"Missing permission: {permission}")
