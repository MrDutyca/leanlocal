# LeanLocal

LeanLocal is a lightweight, privacy-conscious toolkit for understanding what
older and low-spec Linux computers can realistically do.

## Purpose

Useful local computing should not require new hardware, a powerful GPU, or a
permanent cloud connection. LeanLocal provides small, auditable utilities for
basic capability reporting and troubleshooting on ordinary Linux machines.

## Commands

- `leanlocal report` — redacted capability summary.
- `leanlocal bench` — short CPU, memory, and temporary-storage checks.
- `leanlocal check` — read-only dependency/version checks.
- `leanlocal fit` — conservative workload guidance from local resources.
- `leanlocal support` — JSON support bundle you can inspect before sharing.

## Privacy by default

Default output excludes usernames, hostnames, serial numbers, MAC addresses,
IP addresses, Wi-Fi information, account details, file contents, and secrets.
The core toolkit has no telemetry and makes no network requests.

## Design principles

- Standard-library Python wherever practical.
- CPU-first and low-memory.
- Clear, inspectable output.
- No silent uploads or background service.
- Read-only checks unless the user explicitly requests an output file.

## Initial target

Python 3.10+ on Debian/Ubuntu-derived Linux distributions.

## Non-goals

LeanLocal is not a remote-control system, autonomous-agent framework,
workflow engine, orchestration platform, credential manager, or cloud service.

## Status

Pre-release 0.1 candidate. This repository is private until its release gate
has been completed and the exact public contents have been reviewed.
