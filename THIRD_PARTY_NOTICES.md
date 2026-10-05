# Third-party notices / Сторонние компоненты

No vendor DLL or original installer is included in this source-only repository.
`patched/SaiQFFB5.dll`, generated locally by the user, is a modified Saitek/Immersion binary derived from the
Saitek SD6 x64 driver package. Ownership of the original proprietary code
remains with its respective rightsholders; the project MIT license does not
grant rights over that code. The package therefore distributes only newly authored patch code and tools.
Users generate the DLL locally from their own exact supported original using
`build_patch.py`. This packaging does not determine rights under the vendor
EULA or applicable reverse-engineering laws.
Original installers and the WallyCZ binary are not included.

DLL и оригинальные установщики в репозитории отсутствуют. Создаваемая локально
`patched/SaiQFFB5.dll` содержит исходный проприетарный код Saitek/Immersion с
изменениями. MIT-лицензия проекта не распространяется на исходный код
производителя. Право на распространение этого бинарника в ходе работы не
устанавливалось. При публикации можно оставить только патчер и код патча:
пользователь получит ту же DLL из собственного оригинала через `build_patch.py`.
Оригинальные установщики и DLL WallyCZ в комплект не включены.

Prior research / Предшествующая работа:
https://github.com/WallyCZ/saitek-cyborg-ff

The earlier project documents the x64 truncated-pointer problem. This project's
new assembly stubs use a different lookup method and were generated from
analysis of the supplied original DLL; the WallyCZ binary was not used as the
base. Credit for the earlier diagnosis and workaround belongs to that project's
authors. A supplied copy of its binary was later inspected for comparison.
