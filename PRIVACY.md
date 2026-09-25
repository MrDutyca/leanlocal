# Privacy

LeanLocal is designed for local, inspectable operation.

## Default collection

The default capability report contains only:

- operating-system name
- CPU architecture and logical CPU count
- Python version
- total system memory
- total and free root-filesystem capacity

It deliberately excludes hostnames, usernames, serial numbers, hardware
addresses, IP addresses, Wi-Fi details, account information, file contents,
browser data, and credentials.

## Network behaviour

The 0.1 core makes no network requests and contains no telemetry.

## Support bundles

A support bundle contains only the same redacted capability information,
dependency presence/version checks, and generic workload guidance. Users can
open and inspect the JSON file before sharing it.
