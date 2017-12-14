from django.db.models import Case, When
from django.db.models.aggregates import Aggregate, Sum
from django.db.models.fields import IntegerField

__all__ = [
    'CountIfTrue', 'CountIfFalse',
]


class CountIfTrue(Aggregate):
    """
    Counts all cases where provided field is True
    """

    name = 'CountIfTrue'

    def __init__(self, field):
        super().__init__(
            Sum(
                Case(
                    When(**{field: True}, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )


class CountIfFalse(Aggregate):
    """
    Counts all cases where provided field is False
    """

    name = 'CountIfFalse'

    def __init__(self, field):
        super().__init__(
            Sum(
                Case(
                    When(**{field: False}, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
