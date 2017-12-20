from django.db import models
from django.db.models import F


class CarManager(models.Manager):
    def annotate_with_manufactured_country(self):
        return self.annotate(
            country=F('manufacturer__country')
        )


