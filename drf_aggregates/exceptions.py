from rest_framework.exceptions import APIException

__all__ = ['AggregateException', 'QueryException']


class AggregateException(APIException):
    status_code = 422
    default_detail = 'An error has occured in the aggregate API.'
    default_code = 'aggregate_error'


class QueryException(AggregateException):
    status_code = 400
    default_detail = 'Incorrect query parameters.'
