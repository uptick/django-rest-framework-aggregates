import factory
from factory import Faker, SubFactory

from example.models import (
    Manufacturer,
    Car,
)


class ManufacturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manufacturer

    name = Faker('company_suffix')
    country = Faker('country_code')


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    manufacturer = SubFactory(ManufacturerFactory)
    model = Faker('bothify', text="#?", letters="xsuiv")

    manufactured = Faker('past_date')
    classification = factory.Iterator(Car.CLASSIFICATION, getter=lambda c: c[0])
    retail_price = Faker('pydecimal', positive=True, left_digits=5, right_digits=2)
    is_bullet_proof = Faker('pybool')
