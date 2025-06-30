""" python deps for this project """

import config.shared

scripts: dict[str,str] = {
    "pydatacheck": "pydatacheck.main:main",
}

install_requires: list[str] = [
    "pytconf",
    "cinemagoer",
    "beautifulsoup4",
]
build_requires: list[str] = config.shared.PBUILD
test_requires: list[str] = config.shared.PTEST
types_requires: list[str] = [
    "types-PyYAML",
    "types-requests",
]
requires = install_requires + build_requires + test_requires + types_requires
