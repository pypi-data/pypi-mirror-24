"""tests for tvmaze.py"""

import requests
import time
from pytv.tvmaze import Schedule, Show, Season, ApiError
import unittest


class TestSchedule(unittest.TestCase):
    """Tests Schedule class in tvmaze.py"""

    def setUp(self):
        """Creates a schedule"""
        self.schedule = Schedule()

    def test_init_schedule(self):
        """Tests new Schedule class"""

        # test country code default is set to us
        self.assertEqual('US', self.schedule.country_code)
        self.assertTrue(self.schedule.date, time.strftime('%Y-%m-%d'))
        self.assertTrue(self.schedule.url)

    def test_schedule_has_episodes(self):
        """Tests Schedule gets episodes from the tvmaze api"""
        response = requests.get(self.schedule.url)

        # test api returns 200
        self.assertEqual(200, response.status_code)
        shows = self.schedule.episodes

        self.assertTrue(shows)

        # the following tests various things expected in a tvmaze object

        for show in shows:
            self.assertTrue('tvmaze' in show['url'])
            self.assertTrue(all(k in show['show']['schedule'] for k in ['time', 'days']))

    def test_include_networks(self):
        """include_networks() should return all episodes in the included networks"""
        new_episodes = self.schedule.include_networks(['Disney Channel'])
        for episode in new_episodes:
            self.assertTrue(episode["show"]["network"]["name"] in ['Disney Channel'])

    def test_include_multiple_networks(self):
        """include_networks() should return all episodes with multiple networks included"""
        networks = ['Disney Channel', 'HGTV', 'CBS']
        new_episodes = self.schedule.include_networks(networks)
        for episode in new_episodes:
            self.assertTrue(episode["show"]["network"]["name"] in networks)


class TestShow(unittest.TestCase):
    """Tests Show class in tvmaze.py"""

    def test_create_show(self):
        """Tests init method in show class"""
        show = Show(show_id=1)
        self.assertEqual('http://api.tvmaze.com/shows/1', show.api_url)
        self.assertEqual(1, show.id)

    def test_bad_create_show(self):
        """init method of show class should raise error if show id is not valid"""
        self.assertRaises(ApiError, lambda: Show(show_id='3fad'))

    def test_create_show_with_embed_url(self):
        """Tests init method in show class with additional arg embed_url"""
        show = Show(show_id=1, embed_url='?embed=cast')
        self.assertEqual('http://api.tvmaze.com/shows/1?embed=cast', show.api_url)

    def test_episodes(self):
        """episodes property should return a list of episodes"""
        show = Show(show_id=1)
        episodes = show.episodes
        for episode in episodes:
            self.assertTrue('under-the-dome' in episode['url'])

    def test_seasons(self):
        """seasons property should return list of seasons"""
        show = Show(show_id=1)
        self.assertFalse(show.season_list)
        seasons = show.seasons
        self.assertTrue(show.season_list)

        for season in seasons:
            self.assertIsInstance(season, Season)

    def test_specials(self):
        show = Show(show_id=1)
        specials = show.specials
        self.assertTrue(specials)

    def test_failed_episode_by_season_and_number(self):
        """episode_by_number() should raise ValueError if bad season or episode"""
        show = Show(show_id=1)
        self.assertRaises(ValueError, lambda: show.episode_by_number(5, 1))
        self.assertRaises(ValueError, lambda: show.episode_by_number(1, 25))

    def test_episode_by_season_and_number(self):
        """episode_by_number() should return dict of episode information"""
        show = Show(show_id=1)
        episode = show.episode_by_number(1, 1)
        self.assertEqual(1, episode['number'])
        self.assertEqual(1, episode['season'])

        second_episode = show.episode_by_number(2, 11)
        self.assertEqual(2, second_episode['season'])
        self.assertEqual(11, second_episode['number'])

    def test_invalid_date_episode_by_date(self):
        """bad date for episode_by_date() should raise ValueError"""
        show = Show(show_id=1)
        self.assertRaises(ValueError, lambda: show.episodes_by_date('12'))
        self.assertRaises(ValueError, lambda: show.episodes_by_date(''))
        self.assertRaises(ValueError, lambda: show.episodes_by_date(1))
        self.assertRaises(ValueError, lambda: show.episodes_by_date('2002-02-21'))

    def test_valid_date_episode_by_date(self):
        """valid date for episode_by_date() should return list of episodes"""
        show = Show(show_id=1)
        episodes = show.episodes_by_date('2013-07-01')
        for episode in episodes:
            self.assertEqual('2013-07-01', episode['airdate'])

    def test_get_cast(self):
        """get_cast() should return a list of cast members"""
        show = Show(show_id=1)
        self.assertTrue('/1/cast' in show.cast_url)
        self.assertFalse(show.cast_list)
        cast_list = show.cast
        self.assertTrue(show.cast_list)
        self.assertTrue(cast_list)

        for cast in cast_list:
            self.assertTrue('character' in cast)

        for cast in show.cast_list:
            self.assertTrue('character' in cast)

    def test_crew(self):
        """crew property should return list of crew members"""
        show = Show(show_id=1)
        self.assertTrue('/1/crew' in show.crew_url)
        self.assertFalse(show.crew_list)
        crew = show.crew
        self.assertTrue(show.crew_list)
        self.assertTrue(crew)
        for person in crew:
            self.assertTrue('type' in person)


class TestSeason(unittest.TestCase):
    """Tests Season class in tvmaze.py"""

    def test_create_season_with_bad_season(self):
        """Tests init method in Season class"""
        self.assertRaises(ValueError, lambda: Season(season_id='t'))

    def test_season_with_good_season(self):
        """Tests init method in Season class with good season_id"""
        season = Season(season_id=1)
        self.assertTrue(season)

    def test_season_with_episodes(self):
        """Tests init method in Season class with_episodes=True"""
        season = Season(season_id=1, with_episodes=True)
        for episode in season.episodes:
            self.assertEqual(1, episode['season'])

    def test_season_from_kwargs(self):
        """Tests init method from Season class with kwargs instead of season_id"""
        show = Show(show_id=1, embed_url='?embed=seasons')
        season = Season(**show.seasons[0])
        third_season = Season(**show.seasons[-1])
        self.assertTrue('season-1' in season.url)
        self.assertEqual(3, third_season.number)
        self.assertTrue('season-3' in third_season.url)
        self.assertTrue(third_season.episodes)

    def test_episodes(self):
        """Test episodes property"""
        season = Season(season_id=1)

        # make sure episode list empty to ensure season.episodes makes the correct api call
        self.assertFalse(season.episode_list)

        # api call made
        self.assertTrue(season.episodes)

        # make sure episode_list is correctly populated after api call
        self.assertTrue(season.episode_list)
