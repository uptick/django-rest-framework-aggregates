from django.core.urlresolvers import reverse

from example.tests.utils import filter_models, BaseTestCase


class AggregatesAPITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.car_api_url = reverse('car-list')

    def test_countiftrue(self):
        results = self.query_agg_api(
            self.car_api_url,
            'aggregate[CountIfTrue]=is_bullet_proof'
        )
        self.assertIn('countiftrue_is_bullet_proof', results)
        self.assertEqual(
            results['countiftrue_is_bullet_proof'],
            len(filter_models(self.cars, is_bullet_proof=True))
        )

    def test_countiffalse(self):
        results = self.query_agg_api(
            self.car_api_url,
            'aggregate[CountIfFalse]=is_bullet_proof'
        )
        self.assertIn('countiffalse_is_bullet_proof', results)
        self.assertEqual(
            results['countiffalse_is_bullet_proof'],
            len(filter_models(self.cars, is_bullet_proof=False))
        )
