# Changelog

## v0.1.0 — 2026-10-05

- Initial community-testing release; same DLL as the privately tested v0.1 package.
- Resolve truncated x64 effect values using the owner's full-pointer list.
- Reject missing, zero and ambiguous values; preserve the no-download path.
- Add hash-guarded installation, backup and rollback.
- Add reproducible patch generation, assembly sources and 32 native stub tests.
- One user reports working Windows 10 joystick tests, DCS and IL-2 Sturmovik.
- Publish bilingual documentation and test-report templates.

DLL SHA-256: 8a7a9a9d226a50cff6c03028f841a3d2c7a96ba213ec9daa9957669e8013a454
DLL file-version resource: 6.0.4.1 (unchanged).

Первый выпуск для проверки сообществом. DLL совпадает с испытанным пакетом v0.1;
изменения этого выпуска относятся к подготовке репозитория и документации.

### Source-only packaging revision

- Remove the vendor-derived DLL from the public distribution.
- Document local generation from the supported installed original.
- Ignore local generated DLLs in git and diagnose a missing generated DLL.
- Patch behavior and expected output SHA-256 are unchanged.
