"""
Unittest class
"""

import unittest

import requests
from vcr import VCR  # type: ignore

from omdb import OMDB
from omdb.exceptions import OMDBInvalidAPIKey, OMDBNoResults

BUILD_TEST_DATA = False
API_KEY = "supersecret"
RECORD_MODE = "new_episodes" if BUILD_TEST_DATA else "none"


class OMDBOverloaded(OMDB):
    def __init__(self, api_key, timeout=5, strict=True):
        super().__init__(api_key, timeout, strict)

        self.vcr = VCR(
            decode_compressed_response=True,
            record_mode=RECORD_MODE,
            filter_query_parameters=[("apikey", "supersecret"), "api_key"],
            filter_post_data_parameters=[("apikey", "supersecret"), "api_key"],
            path_transformer=VCR.ensure_suffix(".yaml"),
        )

    def _format_results(self, res, params) -> str:
        return super()._format_results(res, params)

    def __build_path(self, kwargs):
        if kwargs["apikey"] == "123456":
            val = kwargs["t"] if "t" in kwargs else kwargs["i"]
            return f"exceptions/bad_api_key/{val}"
        if "t" in kwargs and kwargs["t"] == "Random Movie Title":
            val = kwargs["t"] if "t" in kwargs else kwargs["i"]
            return f"exceptions/no_results/{val}"
        if "type" in kwargs and kwargs["type"] == "series":
            return f"series/{kwargs['t']}"
        if "type" in kwargs and kwargs["type"] == "episode":
            if "Episode" in kwargs:
                return f"episode/{kwargs['t']}/episode-{kwargs['Episode']}"
            return f"episodes/{kwargs['t']}"
        if "s" in kwargs:
            return f"search/{kwargs['s']}"
        print(kwargs)

        return str(kwargs)

    def _get_response(self, kwargs):
        with self.vcr.use_cassette(path=f"./tests/cassettes/{self.__build_path(kwargs)}.yaml"):
            response = requests.get(self._api_url, params=kwargs, timeout=self._timeout).json()
        return self._format_results(response, kwargs)


class TestOMDBSetup(unittest.TestCase):
    def test_api_key(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        self.assertEqual(omdb.api_key, API_KEY)
        self.assertEqual(omdb.strict, True)
        self.assertEqual(omdb.timeout, 5.0)
        self.assertEqual(omdb.api_key, API_KEY)


class TestOMDBExceptions(unittest.TestCase):
    def test_api_key_fail(self):
        self.assertRaises(OMDBInvalidAPIKey, lambda: OMDBOverloaded(api_key=None))
        try:
            OMDBOverloaded(api_key=None)
        except OMDBInvalidAPIKey as ex:
            self.assertEqual(ex.api_key, None)
            self.assertEqual(ex.message, f"Invalid API Key ({ex.api_key}) provided")
        else:
            self.assertEqual(True, False)

    def test_timeout_fail(self):
        self.assertRaises(ValueError, lambda: OMDBOverloaded(api_key=API_KEY, timeout="test"))
        try:
            OMDBOverloaded(api_key=API_KEY, timeout="test")
        except ValueError as ex:
            self.assertEqual(str(ex), "OMDB Timeout must be a float or convertable to float! test provided")
        else:
            self.assertEqual(True, False)

    def test_bad_api_key(self):
        omdb = OMDBOverloaded(api_key="123456")
        self.assertRaises(OMDBInvalidAPIKey, lambda: omdb.get(title="Band of Brothers"))

        try:
            OMDBOverloaded(api_key="123456")
            omdb.get(title="Band of Brothers")
        except OMDBInvalidAPIKey as ex:
            self.assertEqual(str(ex), "Invalid API Key (123456) provided")
        else:
            self.assertEqual(True, False)

    def test_no_results_movie(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        self.assertRaises(OMDBNoResults, lambda: omdb.get(title="Random Movie Title"))

        try:
            omdb = OMDBOverloaded(api_key=API_KEY)
            omdb.get(title="Random Movie Title")
        except OMDBNoResults as ex:
            self.assertEqual(ex.error, "Movie not found!")
        else:
            self.assertEqual(True, False)

    def test_no_results_series(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        self.assertRaises(OMDBNoResults, lambda: omdb.get_series(title="Random Movie Title"))

        try:
            omdb = OMDBOverloaded(api_key=API_KEY)
            omdb.get_series(title="Random Movie Title")
        except OMDBNoResults as ex:
            self.assertEqual(ex.error, "Series not found!")
        else:
            self.assertEqual(True, False)


class TestOMDBSearch(unittest.TestCase):
    def test_search(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search("Band of Brothers")
        self.assertEqual(res["total_results"], "11")


class TestOMDBSeries(unittest.TestCase):
    def test_series(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        bob = omdb.get_series(title="Band of Brothers")

        self.assertEqual(bob["title"], "Band of Brothers")
        self.assertEqual(bob["imdb_id"], "tt0185906")
        self.assertEqual(bob["year"], "2001")
        self.assertEqual(bob["total_seasons"], "1")

        got = omdb.get_series(title="Game of Thrones")
        self.assertEqual(got["title"], "Game of Thrones")
        self.assertEqual(got["imdb_id"], "tt0944947")
        self.assertEqual(got["year"], "2011-2019")
        self.assertEqual(got["total_seasons"], "8")


class TestOMDBEpisodes(unittest.TestCase):
    def test_episodes(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb.get_episodes(title="Band of Brothers", season=1)

    def test_specific_episode(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb.get_episode(title="Band of Brothers", season=1, episode=5)


class TestOMDBMovies(unittest.TestCase):
    pass
