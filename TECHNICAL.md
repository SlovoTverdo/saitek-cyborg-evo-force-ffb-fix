# Implementation notes / Технические сведения

All addresses below are RVAs; the vendor image base is `0x10000000`.

The original effect creation routine allocates an effect, adds it to the owner's
list through RVA `0x7BB0`, and writes the low 32 bits to the output at `0x1679`.
The public 32-bit value is retained: blindly extending its store to 64 bits
could overwrite caller memory. Owner list layout observed in this binary:

| Offset | Meaning |
|---|---|
| owner + 0x10 | Effect count |
| owner + 0x18 | Head node pointer |
| node + 0x00 | Full effect pointer |
| node + 0x08 | Previous node pointer |
| node + 0x10 | Next node pointer |

Six JMP hooks replace the original instructions below:

| Hook RVA | Original bytes | Stub |
|---|---|---|
| 0x1303 | 8B F2 48 8B D9 | patch_1303 |
| 0x13A0 | 41 8B F1 8B DA | patch_13a0 |
| 0x1400 | 85 D2 8B CA 75 | patch_1400 |
| 0x1426 | 85 D2 49 8B D8 8B CA | patch_1426 |
| 0x3156 | 41 8B D8 48 8B F1 | patch_3156 |
| 0x3244 | 4D 8B C1 41 8B D2 | patch_3244 |

The 0x1400 hook replaces the function entry; the remaining original conditional
branch byte is unreachable along the patched entry path. Exact source hashes
and hook bytes are checked before patching.

Stubs scan the list and compare each full effect pointer's low 32 bits to the
incoming value. A second match, no match or zero input returns E_INVALIDARG.
The no-download flag path at 0x1303 is preserved. Device index validation
precedes list access at 0x3156. Device slot stride is 0x580; embedded owner
starts at device + index*0x580 + 0x2B0.

The `.ffbfix` section starts at RVA 0x2E000 and contains relative code, new
UNWIND_INFO records and a sorted copy of the original RUNTIME_FUNCTION table
plus six entries. Stack-neutral mid-function stubs chain to the original
unwind metadata; leaf stubs have leaf records. Real Windows exception-unwind
behavior remains untested. New code makes no imported calls and contains no
absolute image addresses requiring relocation.

The original deletion routine at 0x8550 compares low bits of list-held pointers
and deletes using the full pointer in a node. Its implementation is unchanged.
Additional locking is not added. List lifetime races, low-bit collisions and
reused handles are not solved by a new handle manager. Lookup is O(n).

## Comparison with the supplied WallyCZ DLL

SHA-256: a2fa8aba6b26a408f1fe39270716be88ebda2d191f509058d6bac71a9a27e730
Size: 166912 bytes; added section `.patch` at RVA 0xAA000.

Its binary stubs matched the documented patch.asm. It changes version resources
from 6.0.4.1 to 6.0.4.3; its original exception directory remains unchanged.
Both variants change 34 bytes of original `.text`, but the instructions and
new sections differ. The earlier code reconstructs addresses using high bits
of other registers. In its 0x3156 helper, high bits are taken from RBX, which
is not initialized by the surrounding function before that call. This is a
potential calling-context dependency, not proof of a particular observed crash.

## Русское пояснение

Поле внешнего интерфейса остаётся 32-битным. Исправление ищет полный указатель
в существующем списке; оно не расширяет поле и не добавляет новые идентификаторы.
Изменены шесть участков; размещение вставок и метаданные исключений приведены
выше. Поиск линейный, без дополнительной блокировки списка. Проверка реальных
гонок и исключений в Windows остаётся задачей дальнейших испытаний.
Сравнение с DLL WallyCZ выполнено по бинарнику с указанным SHA-256.
