from django.test import TestCase

from legends.core.models import Season


class TestSeasonTestCase(TestCase):

    def setUp(self):
        # Create some saesons
        for year in range(1994, 2015):
            season = Season(season=year)
            season.save()

        self.seasons = Season.objects.all()

    def test_season_in_range(self):
        years = [s.season for s in self.seasons]

        self.assertIn(1994, years)
        self.assertIn(2000, years)
        self.assertIn(2014, years)

    def test_season_out_of_range(self):
        self.assertRaises(
            Season.DoesNotExist,
            Season.objects.get, **{'season': 1993}
        )
        self.assertRaises(
            Season.DoesNotExist,
            Season.objects.get, **{'season': 2015}
        )

    def test_default_has_full_data(self):
        season = self.seasons[0]
        self.assertTrue(season.has_full_data)

    def test_default_has_no_data(self):
        season = self.seasons[0]
        self.assertFalse(season.has_no_data)



