# ALRYA — Architecture Overview

## High-level architecture

```text
Web Client
React + TypeScript + Vite
        |
        v
FastAPI Application
Python services + route contracts
        |
        +----------------------+
        |                      |
        v                      v
PostgreSQL / Neon         External Integrations
Alembic migrations       Messaging / Ads / PMS / Billing
        |
        v
Multi-tenant domain
Organization → Company → User access → Role → Permission
```

## Tenant model

Tenant context is not treated as a UI-only filter. Organization and company scope participate in the application domain and authorization model.

```text
User
  |
  v
UserCompanyAccess
  |
  +--> Organization
  +--> Company
  +--> Role
  +--> Module permissions
```

## Core engineering boundaries

- The frontend owns presentation, interaction and product state.
- The API owns authentication, authorization, business rules and persistence contracts.
- Migrations version schema changes together with application releases.
- Integrations remain adapters around the product core to reduce provider coupling.
- Applied AI works inside product context instead of as an isolated chat surface.

## Commercial journey

```text
Campaign / Channel → Lead → Conversation → Intent + dates + context
→ Availability → Rate calculation → Quote → Reservation → Revenue
→ Attribution / remarketing / operations
```

This document intentionally omits proprietary implementation details.
