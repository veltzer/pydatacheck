console_scripts = [
    "pydatacheck=pydatacheck.main:main",
]
dev_requires = [
    "pypitools",
    "pydmt",
]
config_requires = []
install_requires = [
    "pytconf",
    "cinemagoer",
    "beautifulsoup4",
]
make_requires = [
    "pyclassifiers",
]
test_requires = [
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
