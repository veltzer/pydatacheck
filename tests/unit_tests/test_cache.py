"""Behavioural tests for pydatacheck's pure caching logic.

The id->data functions memoize into a caller-supplied cache dict and only
reach out to the injected session/getter on a miss. Both paths are exercised
here with fakes, so no network, requests, or imdb access happens.
"""

import unittest
from typing import Any

from pydatacheck import data_check_books, data_check_videos


class _FakeResponse:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def raise_for_status(self) -> None:
        pass


class _RecordingSession:
    """A session whose get() records calls and returns canned HTML."""

    def __init__(self, html: bytes) -> None:
        self._html = html
        self.calls = []

    def get(self, url: str) -> _FakeResponse:
        self.calls.append(url)
        return _FakeResponse(self._html)


class GoodreadsCacheTests(unittest.TestCase):
    def test_cache_hit_does_not_touch_session(self) -> None:
        session = _RecordingSession(b"<html></html>")
        cache = {"123": {"title": "Cached Book"}}
        result = data_check_books.goodreads_id_to_goodreads_data("123", cache, session)
        assert result == {"title": "Cached Book"}
        assert session.calls == []

    def test_cache_miss_fetches_parses_and_stores(self) -> None:
        html = b'<h1 id="bookTitle">  Real Title  </h1>'
        session = _RecordingSession(html)
        cache: dict[str, Any] = {}
        result = data_check_books.goodreads_id_to_goodreads_data("999", cache, session)
        assert result == {"title": "Real Title"}
        # stored for next time, and the fetch went to the /en/ url
        assert cache["999"] == {"title": "Real Title"}
        assert len(session.calls) == 1
        assert "/en/book/show/999" in session.calls[0]


class SimaniaCacheTests(unittest.TestCase):
    def test_cache_hit_does_not_touch_session(self) -> None:
        session = _RecordingSession(b"<html></html>")
        cache = {"77": {"title": "Cached"}}
        result = data_check_books.simania_id_to_simania_data("77", cache, session)
        assert result == {"title": "Cached"}
        assert session.calls == []

    def test_cache_miss_parses_h1(self) -> None:
        session = _RecordingSession(b"<h1> Sefer </h1>")
        cache: dict[str, Any] = {}
        result = data_check_books.simania_id_to_simania_data("77", cache, session)
        assert result == {"title": "Sefer"}
        assert "item_id=77" in session.calls[0]


class ImdbCacheTests(unittest.TestCase):
    def test_cache_hit_does_not_call_getter(self) -> None:
        calls = []

        def getter():
            calls.append(True)
            raise AssertionError("getter must not be called on a cache hit")

        cache = {"tt1": {"title": "Cached Movie"}}
        result = data_check_videos.imdb_id_to_imdb_data("tt1", cache, getter)
        assert result == {"title": "Cached Movie"}
        assert calls == []

    def test_cache_miss_calls_getter_and_stores(self) -> None:
        class FakeCinemagoer:
            @staticmethod
            def get_movie(imdb_id: str) -> dict[str, str]:
                return {"title": f"movie-{imdb_id}"}

        cache: dict[str, Any] = {}
        result = data_check_videos.imdb_id_to_imdb_data("tt2", cache, FakeCinemagoer)
        assert result == {"title": "movie-tt2"}
        assert cache["tt2"] == {"title": "movie-tt2"}
