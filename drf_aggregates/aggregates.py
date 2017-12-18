from django.db.models import Case, When
from django.db.models.aggregates import Sum
from django.db.models.fields import IntegerField

__all__ = [
    'CountIfTrue', 'CountIfFalse',
]


class CountIfTrue(Sum):
    """
    Counts all cases where provided field is True
    """

    def __init__(self, field):
        super().__init__(
            Case(
                When(**{field: True}, then=1),
                default=0,
                output_field=IntegerField()
            )
        )


class CountIfFalse(Sum):
    """
    Counts all cases where provided field is False
    """

    def __init__(self, field):
        super().__init__(
            Case(
                When(**{field: False}, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
