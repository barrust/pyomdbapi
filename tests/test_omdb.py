"""
Unittest class
"""

import os
import unittest

import requests
from dotenv import load_dotenv
from vcr import VCR  # type: ignore

from omdb import OMDB
from omdb.exceptions import OMDBException, OMDBInvalidAPIKey, OMDBLimitReached, OMDBNoResults, OMDBTooManyResults

load_dotenv()

BUILD_TEST_DATA = True
API_KEY = "superscret" if not BUILD_TEST_DATA else os.getenv("OMDB_API_KEY", "supersecret")
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

    def _build_path(self, kwargs):
        if kwargs["apikey"] == "123456":
            val = kwargs["t"] if "t" in kwargs else kwargs["i"]
            return f"exceptions/bad_api_key/{val}"
        if "t" in kwargs and kwargs["t"] == "Random Movie Title":
            val = kwargs["t"] if "t" in kwargs else kwargs["i"]
            return f"exceptions/no_results/{val}"
        if "type" in kwargs and kwargs["type"] == "series":
            if "s" in kwargs:  # searching for series
                return f"search/series/{kwargs['s']}"
            return f"series/{kwargs['t']}"
        if "type" in kwargs and kwargs["type"] == "movie":
            if "s" in kwargs:  # searching for series
                return f"search/movie/{kwargs['s']}"
            val = kwargs["t"] if "t" in kwargs else kwargs["i"]
            return f"movie/{val}"
        if "type" in kwargs and kwargs["type"] == "episode":
            if "Episode" in kwargs:
                return f"episode/{kwargs['t']}/episode-{kwargs['Episode']}"
            return f"episodes/{kwargs['t']}"
        if "s" in kwargs:
            return f"search/{kwargs['s']}"
        # print(kwargs)

        return str(kwargs)

    def _get_response(self, kwargs):
        with self.vcr.use_cassette(path=f"./tests/cassettes/{self._build_path(kwargs)}.yaml"):
            response = requests.get(self._api_url, params=kwargs, timeout=self._timeout).json()
        return self._format_results(response, kwargs)


class TestOMDBSetup(unittest.TestCase):
    def test_api_key(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        self.assertEqual(omdb.api_key, API_KEY)
        self.assertEqual(omdb.strict, True)
        self.assertEqual(omdb.timeout, 5.0)
        self.assertEqual(omdb.api_key, API_KEY)
        self.assertIsNotNone(omdb._session)
        omdb.close()
        self.assertIsNone(omdb._session)


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

    def test_specific_episode_fail(self):
        def tmp_build_path(kwargs):
            return f"exceptions/no_results/{kwargs['t']}"

        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = tmp_build_path

        self.assertRaises(OMDBNoResults, lambda: omdb.get_episode(title="Band of Brothers", season=1, episode=22))

        try:
            omdb.get_episode(title="Band of Brothers", season=1, episode=22)
        except OMDBNoResults as ex:
            self.assertEqual(ex.error, "Series or episode not found!")
        else:
            self.assertEqual(True, False)

    def test_get_missing_title_and_imdbid(self):
        def tmp_build_path(kwargs):
            return "exceptions/base_exception/missing-title-and-imdbid"

        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = tmp_build_path

        self.assertRaises(OMDBException, lambda: omdb.get())

        try:
            omdb.get()
        except OMDBException as ex:
            self.assertEqual(str(ex), "Either title or imdbid is required!")
        else:
            self.assertEqual(True, False)

    def test_too_many_results(self):
        def tmp_build_path(kwargs):
            return "exceptions/too_many_results/A"

        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = tmp_build_path

        self.assertRaises(OMDBTooManyResults, lambda: omdb.search(title="A"))

        try:
            omdb.search(title="A")
        except OMDBTooManyResults as ex:
            self.assertEqual(ex.error, "Too many results.")
            self.assertEqual(ex.params, {"page": 1, "apikey": API_KEY, "s": "A"})
        else:
            self.assertEqual(True, False)

    def test_something(self):
        def tmp_build_path(kwargs):
            return f"exceptions/no_results/{kwargs['i']}"

        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = tmp_build_path

        self.assertRaises(OMDBNoResults, lambda: omdb.get(imdbid="tt596799"))

        try:
            omdb.get(imdbid="tt596799")
        except OMDBNoResults as ex:
            self.assertEqual(ex.error, "Incorrect IMDb ID.")
        else:
            self.assertEqual(True, False)

    def test_limit_reached_error(self):
        def tmp_build_path(kwargs):
            return f"exceptions/limit_reached/{kwargs['s']}"

        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = tmp_build_path

        self.assertRaises(OMDBLimitReached, lambda: omdb.search("order"))
        try:
            omdb.search("order")
        except OMDBLimitReached as ex:
            self.assertEqual(ex.api_key, API_KEY)
            self.assertEqual(ex.message, f"Limit reached for API Key: {omdb.api_key}")


class TestOMDBGet(unittest.TestCase):
    def tmp_build_path(_, kwargs):
        val = kwargs["t"] if "t" in kwargs else kwargs["i"]
        return f"get/{val}"

    def test_get_by_title(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = self.tmp_build_path

        res = omdb.get(title="Despicable Me")
        self.assertEqual(res["imdb_id"], "tt1323594")
        self.assertEqual(res["title"], "Despicable Me")
        self.assertEqual(res["rated"], "PG")

    def test_get_by_imdbid(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        omdb._build_path = self.tmp_build_path

        res = omdb.get(imdbid="tt1323594")
        self.assertEqual(res["imdb_id"], "tt1323594")
        self.assertEqual(res["title"], "Despicable Me")
        self.assertEqual(res["rated"], "PG")


class TestOMDBSearch(unittest.TestCase):
    def test_search(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search("Band of Brothers")
        self.assertEqual(res["total_results"], "11")

    def test_search_page_1(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search("Band of Brothers", pull_all_results=False, page=1)
        self.assertEqual(res["total_results"], "11")
        self.assertEqual(len(res["search"]), 10)

    def test_search_page_2(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search("Band of Brothers", pull_all_results=False, page=2)
        self.assertEqual(res["total_results"], "11")
        self.assertEqual(len(res["search"]), 1)

    def test_search_less_than_10(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search(title="Man From Snowy River")
        self.assertLessEqual(int(res["total_results"]), 10)
        self.assertEqual(res["total_results"], "3")

    def test_search_series(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search_series("malcolm")

        self.assertTrue("Malcolm in the Middle" in [x["title"] for x in res["search"]])
        self.assertEqual(res["total_results"], "18")
        self.assertEqual(len(res["search"]), 18)

    def test_search_movie(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.search_movie("malcolm")

        # get a specific movie
        movie = {}
        for m in res["search"]:
            if m["title"] == "Malcolm" and m["year"] == "1986":
                movie = m
        self.assertEqual(res["total_results"], "88")
        self.assertEqual(len(res["search"]), 88)
        self.assertTrue(movie)
        self.assertEqual(movie["imdb_id"], "tt0091464")


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

    def test_get_series_pull_episodes(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        bsg = omdb.get_series(title="Battlestar Galactica", pull_episodes=True)

        self.assertEqual(bsg["total_seasons"], "4")
        for i in range(1, 5):
            season = bsg["seasons"][i]
            self.assertEqual(season["episodes"][0]["episode"], "1")


class TestOMDBEpisodes(unittest.TestCase):
    def test_episodes(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.get_episodes(title="Band of Brothers", season=1)
        self.assertEqual(res["total_seasons"], "1")
        self.assertEqual(len(res["episodes"]), 10)

        res = omdb.get_episodes(title="Psych", season=3)
        self.assertEqual(res["total_seasons"], "8")
        self.assertEqual(len(res["episodes"]), 16)

    def test_specific_episode(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        res = omdb.get_episode(title="Band of Brothers", season=1, episode=5)
        self.assertEqual(res["title"], "Crossroads")
        self.assertEqual(res["year"], "2001")

        res = omdb.get_episode(title="Psych", season=3, episode=10)
        self.assertEqual(res["title"], "Six Feet Under the Sea")
        self.assertEqual(res["year"], "2009")


class TestOMDBMovies(unittest.TestCase):
    def test_get_movie(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        mov = omdb.get_movie(title="Apollo 13")
        self.assertEqual(mov["year"], "1995")
        self.assertEqual(mov["director"], "Ron Howard")
        self.assertEqual(mov["runtime"], "140 min")
        self.assertEqual(mov["imdb_id"], "tt0112384")

    def test_get_movie_imdb_id(self):
        omdb = OMDBOverloaded(api_key=API_KEY)
        mov = omdb.get_movie(imdbid="tt0190332")
        self.assertEqual(mov["year"], "2000")
        self.assertEqual(mov["director"], "Ang Lee")
        self.assertEqual(mov["runtime"], "120 min")
        self.assertEqual(mov["title"], "Crouching Tiger, Hidden Dragon")
