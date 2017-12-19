from django.core.urlresolvers import reverse

from example.models import Car
from example.tests.utils import filter_models, BaseTestCase


class AggregatesAPITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.car_api_url = reverse('car-list')

    def test_default(self):
        results = self.query_agg_api(self.car_api_url)
        self.assertEqual(len(results), len(self.cars))

    def test_group_by(self):
        results = self.query_agg_api(
            self.car_api_url,
            'group_by[classification]'
        )
        self.assertIn('classification', results[0])

        # we make sure that group by returns all group by categories
        expectedKeys = set(sorted([x[0] for x in Car.CLASSIFICATION]))
        resultKeys = set(sorted([x['classification'] for x in results]))
        self.assertEqual(expectedKeys, resultKeys)

    def test_group_by_and_count(self):
        results = self.query_agg_api(
            self.car_api_url,
            'group_by[manufacturer__name]',
            'group_by[manufacturer__id]',
            'aggregate[Count]=id',
        )
        for row in results:
            count_cars = len(filter_models(
                self.cars, manufacturer_id=row['manufacturer__id']
            ))
            self.assertEqual(count_cars, row['count_id'])

    def test_group_by_and_choice_fields(self):
        results = self.query_agg_api(
            self.car_api_url,
            'group_by[classification]',
            'aggregate[Count]=id',
        )

        # choice fields both return the database key and the display value
        self.assertIn('classification', results[0])
        self.assertIn('classification_display', results[0])

        # check that the group by count worked
        for row in results:
            count_cars = len(filter_models(
                self.cars, classification=row['classification']
            ))
            self.assertEqual(count_cars, row['count_id'])

            # check that the display value is correct
            self.assertEqual(
                row['classification_display'],
                dict(Car.CLASSIFICATION).get(row['classification'])
            )

