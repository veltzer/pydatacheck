"""
Check that .yaml files have correct names of movies
"""


import importlib.util
import pkgutil
import shelve

import yaml


def _get_cinemagoer_class():
    """ import Cinemagoer lazily, shimming pkgutil.find_loader for Python 3.14+ """
    # cinemagoer (imdb) still uses pkgutil.find_loader, removed in Python 3.14
    if not hasattr(pkgutil, "find_loader"):
        pkgutil.find_loader = importlib.util.find_spec
    from imdb import Cinemagoer  # type: ignore  # pylint: disable=import-outside-toplevel
    return Cinemagoer


def imdb_id_to_imdb_data(f_imdb_id, cache, get_cinemagoer):
    """ cached version of getting title by imdb """
    if f_imdb_id in cache:
        obj = cache[f_imdb_id]
    else:
        print(f"retrieving [{f_imdb_id}]...")
        obj = get_cinemagoer().get_movie(f_imdb_id)
        cache[f_imdb_id] = obj
    return obj


def do_check_videos(files_to_check):
    """ main entry point """
    shelve_filename = "imdb_id_to_imdb_data.shelve"
    with shelve.open(shelve_filename) as cache:
        # Built lazily: constructing Cinemagoer needs a local IMDb dataset
        # (current releases only ship the "s3" access system, and its default
        # URI is the malformed `sqlite://cinemagoer.db`). When every id is
        # already in the shelve — the normal case in CI — no instance is
        # needed at all, so only an actual cache miss pays that cost.
        cinemagoer_instance = []

        def get_cinemagoer():
            if not cinemagoer_instance:
                cinemagoer_instance.append(_get_cinemagoer_class()())
            return cinemagoer_instance[0]

        for file_to_check in files_to_check:
            # print(f"checking [{file_to_check}]")
            with open(file_to_check, encoding="utf-8") as stream:
                data = yaml.safe_load(stream)
            data = data["items"]
            for datum in data:
                f_imdb_id = datum["imdb_id"]
                f_name = datum["name"]
                # print(f"doing [{f_name}] [{f_imdb_id}]")
                imdb_data = imdb_id_to_imdb_data(f_imdb_id, cache, get_cinemagoer)
                f_title = imdb_data["title"]
                assert f_title == f_name, f"{f_imdb_id} {f_title} {f_name}"
