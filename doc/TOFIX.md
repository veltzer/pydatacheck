# TOFIX

Findings from a code scan on 2026-10-04.

## Medium

- `src/pydatacheck/data_check_books.py:31` - on a parse failure the page is dumped to the fixed path `/tmp/temp.html` (also line 52), which is predictable (symlink/clobber risk on a shared host), overwritten by every failure, and opened without `encoding=`; write it with `tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")` and print the path in the error.
- `src/pydatacheck/data_check_books.py:97` - data mismatches are reported with `assert` (also lines 33, 54, 104, 108 and `data_check_videos.py:62`), so running under `python -O` silently disables every check this tool exists to perform; raise a real exception (or collect errors and exit non-zero).
- `src/pydatacheck/data_check_books.py:21` - `session.get(url)` has no `timeout` (also line 42), so a stalled goodreads/simania connection hangs the check forever; pass an explicit `timeout=`.

## Low

- `src/pydatacheck/data_check_videos.py:17` - the `pkgutil.find_loader` shim is dead: the locked `cinemagoer` (2026.8.20) no longer references `find_loader` anywhere and `from imdb import Cinemagoer` imports fine on Python 3.14 without it; remove the shim and the docstring/comment at lines 15-16.
- `src/pydatacheck/data_check_books.py:9` - `import bs4  # type: ignore` is unnecessary: the locked beautifulsoup4 4.15 ships `py.typed` and mypy passes without the suppression; drop it.
- `src/pydatacheck/data_check_books.py:13` - `CHEKC_ID_FOR_EVERY_BOOK` is misspelled (`CHECK_...`), and the commented-out `print` debug lines (17, 23, 40, 44, 85; `data_check_videos.py:52, 59`) are leftovers; rename and delete them.
- `src/pydatacheck/route.py:4` - `accept()` and `src/pydatacheck/configs.py:9` `ConfigRoute` are never referenced anywhere in the package; delete both modules and their sections in `sphinx/pydatacheck.rst:7-13,39-45`.
- `pyproject.toml:102` - the dev group repeats `pylogconf`, `pyyaml` and `requests`, which are already runtime dependencies (lines 39-41); remove the duplicates.
- `doc/TODO.txt:1` - the file is empty; delete it.
