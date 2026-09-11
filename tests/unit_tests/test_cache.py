"""Behavioural tests for pydatacheck's pure caching logic.

The id->data functions memoize into a caller-supplied cache dict and only
reach out to the injected session/getter on a miss. Both paths are exercised
here with fakes, so no network, requests, or imdb access happens.
"""

import unittest

from pydatacheck import data_check_books, data_check_videos


class _FakeResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        pass


class _RecordingSession:  # pylint: disable=too-few-public-methods
    """A session whose get() records calls and returns canned HTML."""

    def __init__(self, html):
        self._html = html
        self.calls = []

    def get(self, url):
        self.calls.append(url)
        return _FakeResponse(self._html)


class GoodreadsCacheTests(unittest.TestCase):
    def test_cache_hit_does_not_touch_session(self):
        session = _RecordingSession(b"<html></html>")
        cache = {"123": {"title": "Cached Book"}}
        result = data_check_books.goodreads_id_to_goodreads_data("123", cache, session)
        self.assertEqual(result, {"title": "Cached Book"})
        self.assertEqual(session.calls, [])

    def test_cache_miss_fetches_parses_and_stores(self):
        html = b'<h1 id="bookTitle">  Real Title  </h1>'
        session = _RecordingSession(html)
        cache = {}
        result = data_check_books.goodreads_id_to_goodreads_data("999", cache, session)
        self.assertEqual(result, {"title": "Real Title"})
        # stored for next time, and the fetch went to the /en/ url
        self.assertEqual(cache["999"], {"title": "Real Title"})
        self.assertEqual(len(session.calls), 1)
        self.assertIn("/en/book/show/999", session.calls[0])


class SimaniaCacheTests(unittest.TestCase):
    def test_cache_hit_does_not_touch_session(self):
        session = _RecordingSession(b"<html></html>")
        cache = {"77": {"title": "Cached"}}
        result = data_check_books.simania_id_to_simania_data("77", cache, session)
        self.assertEqual(result, {"title": "Cached"})
        self.assertEqual(session.calls, [])

    def test_cache_miss_parses_h1(self):
        session = _RecordingSession(b"<h1> Sefer </h1>")
        cache = {}
        result = data_check_books.simania_id_to_simania_data("77", cache, session)
        self.assertEqual(result, {"title": "Sefer"})
        self.assertIn("item_id=77", session.calls[0])


class ImdbCacheTests(unittest.TestCase):
    def test_cache_hit_does_not_call_getter(self):
        calls = []

        def getter():
            calls.append(True)
            raise AssertionError("getter must not be called on a cache hit")

        cache = {"tt1": {"title": "Cached Movie"}}
        result = data_check_videos.imdb_id_to_imdb_data("tt1", cache, getter)
        self.assertEqual(result, {"title": "Cached Movie"})
        self.assertEqual(calls, [])

    def test_cache_miss_calls_getter_and_stores(self):
        class FakeCinemagoer:  # pylint: disable=too-few-public-methods
            @staticmethod
            def get_movie(imdb_id):
                return {"title": f"movie-{imdb_id}"}

        cache = {}
        result = data_check_videos.imdb_id_to_imdb_data("tt2", cache, FakeCinemagoer)
        self.assertEqual(result, {"title": "movie-tt2"})
        self.assertEqual(cache["tt2"], {"title": "movie-tt2"})
