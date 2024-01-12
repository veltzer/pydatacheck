from typing import List


console_scripts: List[str] = [
    "pydatacheck=pydatacheck.main:main",
]
dev_requires: List[str] = [
    "pymultigit",
    "pypitools",
    "black",
]
config_requires: List[str] = [
    "pyclassifiers",
]
install_requires: List[str] = [
    "pytconf",
    "cinemagoer",
    "beautifulsoup4",
]
make_requires: List[str] = [
    "pydmt",
]
test_requires: List[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "flake8",
    "pymakehelper",
    "mypy",
    "types-PyYAML",
    "types-requests",
]
requires = config_requires + install_requires + make_requires + test_requires
