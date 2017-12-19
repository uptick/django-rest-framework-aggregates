import json
import random

from rest_framework.test import APITestCase

from example.factories import CarFactory, ManufacturerFactory


def filter_models(model_list, **filters):
    return [
        obj for obj in model_list
        if all([getattr(obj, key) == val for key, val in filters.items()])
    ]


class BaseTestCase(APITestCase):
    def setUp(self):
        super().setUp()

        # we fix the number of manufacturers so that we can group by nicely
        # (rather than each cars having a different manufacturer)
        num_manufacturers = random.randint(3, 5)
        self.manufacturers = [ManufacturerFactory() for x in range(0, num_manufacturers)]
        self.cars = [
            CarFactory(manufacturer=self.manufacturers[random.randint(0, num_manufacturers - 1)])
            for x in range(0, random.randint(20, 50))
        ]

    def query_agg_api(self, root, *params):
        query = '&'.join(params)
        response = self.client.get(f'{root}?format=agg&{query}')
        self.assertEqual(response.status_code, 200, response.data)
        return json.loads(response.data)['data']