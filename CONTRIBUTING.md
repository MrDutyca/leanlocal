# Contributing

LeanLocal aims to remain small, auditable, and useful on modest Linux hardware.

## Before opening a change

- Keep runtime dependencies at zero unless there is a strong documented reason.
- Do not add telemetry, automatic uploads, accounts, or background services.
- Do not collect identifying system or network information by default.
- Prefer read-only checks and explicit user actions.
- Keep benchmarks short enough for low-spec machines.

## Pull requests

Explain the user problem, the change, resource impact, privacy impact, and tests.
Small focused changes are preferred.

## Security

Do not disclose a suspected vulnerability in a public issue. Follow SECURITY.md.
