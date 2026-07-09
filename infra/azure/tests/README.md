# Azure Infrastructure Tests

These scripts validate Azure infrastructure after deployment.

Current tests:

- 01 - Storage Account connectivity
- 02 - Blob upload
- 03 - Blob listing
- 04 - Blob download
- 99 - Run all tests

Security rules:

- Never print connection strings.
- Never print storage keys.
- Never print Azure secrets.
- Tests should clean temporary files after execution whenever possible.