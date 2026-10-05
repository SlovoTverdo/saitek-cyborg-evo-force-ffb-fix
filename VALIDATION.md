# Validation

2026-10-05: assembly and symbol manifest reproduce exactly; original DLL produces the exact shipped patched DLL; all 32 native stub cases passed.

User reports: Windows 10 joystick effects, DCS and IL-2 Sturmovik working. Detailed game builds and executable bitness not recorded. No automated hardware tests; real exception unwinding and concurrent list mutation untested.

PowerShell installer has not been exercised in an automated Windows test environment; its installation path was used successfully by the reporting user.

Source-only revision: no DLL/SYS/EXE or original package distributed. Local patch generation still produces the tested DLL hash. Installer missing-output check added; not tested in Windows.
