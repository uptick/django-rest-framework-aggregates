from django.core.urlresolvers import reverse

from example.models import Car
from example.tests.utils import filter_models, BaseTestCase


class AggregatesAPITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.car_api_url = reverse('car-list')

    def test_count(self):
        results = self.query_agg_api(
            self.car_api_url,
            'aggregate[Count]=id'
        )
        self.assertIn('count_id', results)
        self.assertEqual(results['count_id'], len(self.cars))

        # we test that filtering works in conjuction with our aggregates
        classification = Car.CLASSIFICATION[0][0]
        results = self.query_agg_api(
            self.car_api_url,
            f'classification={classification}',
            'aggregate[Count]=id',
        )
        self.assertIn('count_id', results)
        self.assertEqual(
            results['count_id'],
            len(filter_models(self.cars, classification=classification))
        )

    def test_min(self):
        classification = Car.CLASSIFICATION[0][0]
        results = self.query_agg_api(
            self.car_api_url,
            'aggregate[Min]=retail_price'
        )
        self.assertIn('min_retail_price', results)
        self.assertEqual(
            results['min_retail_price'],
            float(min([x.retail_price for x in self.cars]))
        )

    def test_max(self):
        results = self.query_agg_api(
        self.car_api_url,
        'aggregate[Max]=retail_price'
    )
        self.assertIn('max_retail_price', results)
        self.assertEqual(
            results['max_retail_price'],
            float(max([x.retail_price for x in self.cars]))
        )

    def test_sum(self):
        results = self.query_agg_api(
        self.car_api_url,
        'aggregate[Sum]=retail_price'
    )
        self.assertIn('sum_retail_price', results)
        self.assertEqual(
            results['sum_retail_price'],
            float(sum([x.retail_price for x in self.cars]))
        )