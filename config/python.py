""" python deps for this project """

scripts: dict[str,str] = {
    "pydatacheck": "pydatacheck.main:main",
}
config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
    "pytconf",
    "cinemagoer",
    "beautifulsoup4",
]
build_requires: list[str] = [
    "pydmt",
    "pymakehelper",
]
test_requires: list[str] = [
    "pylint",
    "pytest",
    "mypy",
    "ruff",
    # types
    "types-PyYAML",
    "types-requests",
]
requires = config_requires + install_requires + build_requires + test_requires
