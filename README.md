# Saitek Cyborg Evo Force — x64 Force Feedback Fix

[English](#english) | [Русский](#русский)

## English

An experimental patch for the **64-bit Force Feedback DLL of the Saitek Cyborg
Evo Force**, tested by one user on Windows 10 in the joystick control panel,
DCS and IL-2 Sturmovik. It fixes handling of truncated effect pointers without
replacing Windows `pid.dll`.

**Status: v0.1.0 — community testing.** This is a patch to a vendor user-mode
DLL, not a new kernel or USB driver. Wider compatibility is not established.

### Reported results

| Environment | Result reported on October 4–5, 2026 |
|---|---|
| Windows 10 joystick properties | Effects work; no crashes reported |
| DCS | Force Feedback works |
| IL-2 Sturmovik | Force Feedback works |

Across the simulator tests, the user reported stall buffet, weapon/release
feedback and bumps while taking off from an unpaved surface. These are physical
user observations, not automated assertions. Exact simulator builds, aircraft,
IL-2 edition and executable bitness were not recorded. These reports do not
prove that every effect type, aircraft or game is supported.

### Supported original

- Device: **Saitek Cyborg Evo Force**, VID `06A3`, PID `FFB5`.
- Package: Saitek SD6 x64; INF `DriverVer=05/01/2007,6.0.4.1`.
- Target: original **x64** `SaiQFFB5.dll`, 162,816 bytes.
- Only the exact original SHA-256 below is accepted.

```text
Original:
fbf17423e5cd778cd8d59768c5cbb71d3a24447eb7c34fbca8379b0f11dcaf5e
Patched v0.1.0:
8a7a9a9d226a50cff6c03028f841a3d2c7a96ba213ec9daa9957669e8013a454
```

The patched file is 172,032 bytes. Its Windows file-version resource remains
**6.0.4.1**; use the SHA-256 to identify this patch. 32-bit `Sai2FFB5.dll` is
unchanged. Other device models, driver versions and Windows 11 are untested.

### Install

1. Have the supported original Saitek SD6 x64 driver installed. If testing an
   alternative FFB driver, finish that test and return to the original Saitek
   configuration first. This script does not set up COM registration or install
   the vendor package.
2. Download and extract the complete project ZIP. **No vendor DLL is included.**
   Install Python 3 if needed, then run from the extracted directory:

   ```powershell
   New-Item -ItemType Directory -Path .\patched -Force
   python .\build_patch.py "$env:SystemRoot\System32\SaiQFFB5.dll" .\patched\SaiQFFB5.dll
   ```

   The patcher reads your installed original and writes a separate local copy;
   it does not modify System32. It rejects any unsupported original. You can
   instead pass a supported original DLL extracted from your own installer.
3. Close games, `joy.cpl` and all applications using the joystick.
4. Open **64-bit Windows PowerShell as Administrator**, change to the extracted
   directory, then run:

   ```powershell
   .\Install.ps1
   ```

   If local policy blocks the script, a session-only option is:

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\Install.ps1
   ```

5. The script verifies the installed DLL's hash, backs it up as
   `SaiQFFB5.dll.codex-v01-original.bak` next to it, and replaces only
   `%SystemRoot%\System32\SaiQFFB5.dll`. It also verifies the copied file.
6. Reconnect the joystick and restart the test application. Start with low
   FFB strength, such as 10–20%.

The script refuses unsupported DLLs, including a previous third-party patch.
A file in System32 alone does not prove correct COM registration. If copying
fails because the DLL is in use, close the holding application or reboot.
No Windows system DLLs, registry entries, SYS, INF or CAT files are modified.

### Roll back

Close joystick applications and run from the same directory in an elevated
64-bit PowerShell:

```powershell
.\Install.ps1 -Restore
```

The script verifies both the installed patch and the original backup before
restoring. Keep the backup. Vendor driver reinstallation may restore the old
DLL; this project does not block Windows maintenance or updates.

### What changed

The original DLL stores a 64-bit effect pointer into a 32-bit output field at
RVA `0x1679`. Full addresses are still present in the owner's internal linked
list. The new stubs resolve the 32-bit value against that list, returning the
stored full pointer only for a unique match. Missing, zero or ambiguous values
are rejected with `E_INVALIDARG` rather than interpreted as arbitrary addresses.

The earlier [WallyCZ patch](https://github.com/WallyCZ/saitek-cyborg-ff) mainly
reconstructs high address bits using other pointers. This patch uses the stored
list instead, so it does not assume that owner and effect allocations share the
same aligned 4-GiB address range. See [technical details](TECHNICAL.md).

### Limitations and validation

- One user has tested the physical joystick; broader reports are welcome.
- 32 native x64 machine-code cases passed on Linux with synthetic lists and
  mocked continuation points. These are not Windows/USB integration tests.
- Reproducible output, input rejection, hook scope and PE exception-table
  ordering/ranges were checked.
- Additional synchronization of the list was not added. Concurrent effect
  creation/deletion races remain untested.
- Low-32-bit pointer collisions are rejected, not eliminated by a new ID scheme.
- New unwind records were added, but actual Windows exception unwinding has not
  been tested. Windows loader operation is supported by the user's working
  installation; detailed loader diagnostics were not collected.

### Build and test

Python 3 is sufficient to patch your own supported original (no extra Python
packages). Existing output files are never overwritten:

```powershell
python .\build_patch.py .\original\SaiQFFB5.dll .\new-SaiQFFB5.dll
```

To rebuild the assembly code and symbol manifest, use Python 3 and GNU binutils
on Linux x64:

```bash
python3 rebuild.py
```

To run the native instruction tests:

```bash
gcc -shared -fPIC -o test_bridge.so test_bridge.S
python3 test_native.py
```

If assembly is changed, update the release hash in `Install.ps1`, this README
and `SHA256SUMS.txt` after generating and validating the new DLL. Do not use the
old installer hash for a new binary.

### Feedback, credits and licensing

Use the issue templates for successful tests or bugs. Please include Windows
version, DLL hash, application/edition/build, executable bitness if known,
working/missing effects, crashes and reproduction steps. Do not upload private
logs without reviewing their contents.

Initiated and physically tested by **Sergey**; patch code and analysis developed
with **OpenAI ChatGPT / Codex**. Thanks to WallyCZ and the earlier community
research for documenting the problem and workaround. This project is independent
of Saitek, Immersion and WallyCZ; no endorsement is implied.

New code, tests and documentation: MIT. No vendor DLL is distributed in this repository. Locally generated vendor DLL code is outside that license;
see [third-party notices](THIRD_PARTY_NOTICES.md).

## Русский

Экспериментальный патч **64-разрядной FFB-библиотеки Saitek Cyborg Evo Force**.
Один пользователь проверил его на Windows 10 в свойствах джойстика, DCS и
«Ил-2 Штурмовик». Патч исправляет обработку обрезанных адресов эффектов без
замены системного `pid.dll`.

**Статус: v0.1.0 — проверка сообществом.** Это исправление пользовательской DLL
производителя; новый USB-драйвер или драйвер ядра не устанавливается.

### Подтверждённые пользователем результаты

| Среда | Результат, сообщённый 4–5 октября 2026 года |
|---|---|
| Свойства джойстика Windows 10 | Эффекты работают, вылетов не было |
| DCS | Обратная связь работает |
| «Ил-2 Штурмовик» | Обратная связь работает |

При проверке симуляторов ощущались тряска при срыве потока, отдача при
применении вооружения и сбросе подвесок, кочки при взлёте с грунта. Это результаты
ручной проверки настоящего устройства. Точные сборки, самолёты, редакция Ил-2
и разрядность приложений не записаны. Проверка не подтверждает поддержку всех
эффектов, самолётов и игр.

### Совместимость

- Устройство: **Saitek Cyborg Evo Force**, VID `06A3`, PID `FFB5`.
- Исходный пакет: SD6 x64, INF `DriverVer=05/01/2007,6.0.4.1`.
- Исходная **x64** `SaiQFFB5.dll`: 162 816 байт; исправленная: 172 032 байта.
- Поддерживается только точный SHA-256 оригинала, указанный в английской части.
- Версия в ресурсах исправленной DLL осталась **6.0.4.1**. Определяй патч по
  SHA-256. 32-битная `Sai2FFB5.dll` не меняется.
- Другие модели, версии драйверов и Windows 11 не проверены.

### Установка

1. Должен быть установлен поддерживаемый оригинальный Saitek SD6 x64. Если
   пробовал альтернативный FFB-драйвер, сначала верни исходную конфигурацию
   Saitek. Скрипт не устанавливает пакет и не настраивает COM-регистрацию.
2. Скачай и распакуй весь ZIP. **DLL производителя в архиве нет.**
   Установи Python 3 при необходимости и из папки проекта выполни:

   ```powershell
   New-Item -ItemType Directory -Path .\patched -Force
   python .\build_patch.py "$env:SystemRoot\System32\SaiQFFB5.dll" .\patched\SaiQFFB5.dll
   ```

   Патчер читает установленный оригинал и создаёт отдельную локальную копию;
   System32 на этом шаге не меняется. Другую версию он отвергнет. Можно также
   передать поддерживаемую DLL, извлечённую из собственного установщика.
3. Закрой игры, `joy.cpl` и программы с джойстиком.
4. Открой **64-битную Windows PowerShell от администратора**, перейди в папку
   проекта и выполни:

   ```powershell
   .\Install.ps1
   ```

   Если выполнение запрещено политикой, можно разрешить его только в текущем
   окне:

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\Install.ps1
   ```

5. Скрипт проверит хеш оригинала, сохранит рядом резервную копию
   `SaiQFFB5.dll.codex-v01-original.bak` и заменит только
   `%SystemRoot%\System32\SaiQFFB5.dll`, затем проверит результат.
6. Переподключи джойстик и перезапусти тестовую программу. Начни с небольшой
   силы, например 10–20%.

Другую версию DLL или чужой патч скрипт заменять откажется. Наличие DLL в
System32 ещё не доказывает правильную регистрацию. Если файл занят, закрой
использующую его программу или перезагрузи Windows. Системные DLL Windows,
реестр, SYS, INF и CAT не меняются.

### Откат

Закрой программы с джойстиком и в административной 64-битной PowerShell из
папки проекта выполни:

```powershell
.\Install.ps1 -Restore
```

Скрипт проверяет хеши патча и резервной копии. Сохрани резервную копию.
Переустановка драйвера производителя может вернуть старую DLL; патч не
блокирует обслуживание и обновления Windows.

### Отличие от прежнего исправления

Оригинальная DLL записывает 64-битный указатель эффекта в 32-битное выходное
поле по RVA `0x1679`, хотя полный адрес сохраняется во внутреннем связанном
списке. Наш код ищет полный адрес в этом списке и требует единственное
совпадение. Нулевое значение, отсутствие эффекта и неоднозначность дают
`E_INVALIDARG`.

Прежний [патч WallyCZ](https://github.com/WallyCZ/saitek-cyborg-ff) в основном
заимствует старшие биты других указателей. Наш поиск не требует одинаковых
старших битов адресов владельца и эффекта. Подробности: [TECHNICAL.md](TECHNICAL.md).

### Проверки и ограничения

- Аппаратные проверки пока выполнены одним пользователем.
- Прошли 32 проверки самих x64-вставок в Linux с искусственными списками и
  имитацией конечных функций. Они не проверяют Windows, USB или моторы.
- Проверены воспроизводимость DLL, отказ для неподдерживаемого оригинала,
  область правок и структура таблицы исключений PE.
- Дополнительная синхронизация списка не введена: гонки при одновременном
  создании и удалении эффектов требуют проверки.
- Коллизии младших 32 бит обнаруживаются, но новый механизм ID не добавлен.
- Для вставок добавлены unwind-записи, но раскрутка стека при исключении в
  Windows не проверена. DLL успешно используется пользователем; подробные
  диагностические данные загрузчика не собирались.

### Сборка, отзывы и авторство

Патчер требует Python 3 без дополнительных пакетов:

```powershell
python .\build_patch.py .\original\SaiQFFB5.dll .\new-SaiQFFB5.dll
```

Существующий выходной файл не перезаписывается. Пересборка вставок:
`python3 rebuild.py` в Linux с GNU binutils. Нативные тесты запускаются командами
из английской части. При изменении DLL обнови хеши в установщике и документации.

Присылай через Issues успешные проверки и ошибки: версия Windows, хеш DLL,
игра/редакция/сборка, разрядность при наличии данных, работающие и отсутствующие
эффекты, вылеты и шаги воспроизведения.

Инициатор и аппаратный тестировщик — **Сергей**. Код патча и анализ подготовлены
совместно с **OpenAI ChatGPT / Codex**. Благодарность WallyCZ и сообществу за
предшествующее исследование. Проект независим от Saitek, Immersion и WallyCZ.
Новый код и документация — MIT; исходный код производителя в локально созданной DLL этой лицензией
не покрывается. См. [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
