# ALRYA — Public Technical Showcase

> Public technical documentation for a proprietary product. The production source code remains private.

## Overview

ALRYA is a multi-tenant SaaS platform for hospitality operations. It connects acquisition, conversations, quotation, reservation, revenue, marketing operations and applied AI in a shared operational journey.

This public repository demonstrates product and engineering work without publishing proprietary implementation details.

## What this showcase demonstrates

- Product architecture and module boundaries.
- Frontend: React, TypeScript and Vite.
- Backend: FastAPI and Python.
- Data: PostgreSQL/Neon with Alembic migrations.
- Multi-tenant context using organizations, companies, user access, roles and permissions.
- JWT authentication and module-level authorization.
- CI, tests, health checks and deployment discipline.
- Product flows from campaign origin to revenue attribution.
- Engineering decisions, trade-offs and security boundaries.

## Product flow

```text
Campaign → Lead → Conversation → Context → Availability → Rate Engine → Quote → Reservation → Revenue
```

## Main modules

Revenue · Omnichannel Chats · Assistant · Agents · Marketing · Studio · Integrations · Billing · Admin · Tracker

## Documentation

- [Architecture](docs/architecture.md)
- [Product scope](docs/product.md)
- [Security and privacy](docs/security.md)

## Public here

Architecture, technology choices, module responsibilities, technical flows, product reasoning, validation strategy and non-sensitive diagrams.

## Private by design

Production source code, proprietary business logic, Rate Engine implementation, internal prompts, customer data, credentials, tokens, webhook secrets and provider-specific production configuration.

## Code samples

The `examples/` directory contains **sanitized, representative code written specifically for public evaluation**. It mirrors engineering concerns from the product—tenant isolation, permission checks, API boundaries, typed frontend access and tests—without copying the production implementation.

- [Examples overview](examples/README.md)
- [Tenant-aware domain service](examples/backend/domain.py)
- [FastAPI adapter](examples/backend/app.py)
- [Backend tests](examples/backend/test_tenant_access.py)
- [Typed frontend client](examples/frontend/revenue-client.ts)

These samples use synthetic names, data and endpoints. They are not a deployable copy of ALRYA.

## Portfolio case

[Open the full public case](https://mateus-nascimento-dev.lovable.app/projetos/alrya)

## Author

Mateus Nascimento dos Santos · [GitHub](https://github.com/matteusnascimento)

---

**This showcase is documentation, not the production repository.**
