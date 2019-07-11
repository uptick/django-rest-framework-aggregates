import json
from itertools import chain

from django.db.models import Case, CharField, Value, When
from django.db.models.aggregates import Aggregate, Avg, Count, Max, Min, StdDev, Sum, Variance
from django.db.models.fields import DateField, FieldDoesNotExist
from django.db.models.functions import Extract, TruncDate
from rest_framework import renderers
from rest_framework.utils import encoders

from .aggregates import CountIfFalse, CountIfTrue
from .exceptions import AggregateException, QueryException

__all__ = ['AggregateRenderer', ]

AGGREGATE_FNS = {
    # default django functions
    'Aggregate': Aggregate,
    'Avg': Avg,
    'Count': Count,
    'Max': Max,
    'Min': Min,
    'StdDev': StdDev,
    'Sum': Sum,
    'Variance': Variance,
    # custom aggregate functions
    'CountIfTrue': CountIfTrue,
    'CountIfFalse': CountIfFalse,
}

_AGGREGATE_KEYWORD = 'aggregate'
_GROUPBY_KEYWORD = 'group_by'


class AggregateRenderer(renderers.BaseRenderer):
    '''
    Main renderer for the aggregate functions
    '''
    media_type = 'application/json'
    format = 'agg'

    def _clean_agg_query_params(self, query_params, keyword):
        '''
        Checks the supplied query_params object for keys containing the supplied keyword
        and parses the query_params to return a dictionary of arg: value where the query_param
        is keyword[arg]=value. Handles multiple instances of keyword[arg].
        '''
        try:
            cleaned_matches = {
                key[key.index('[') + 1: key.index(']')]: list(
                    chain.from_iterable([x.split(',') for x in query_params.getlist(key)])
                ) for key in query_params.keys() if keyword in key
            }
        except ValueError as e:
            raise QueryException(
                f'Unable to parse query parameters for {keyword}.\n {e}'
            )

        return cleaned_matches

    def render(self, data, media_type=None, renderer_context=None):
        '''
        Render queryset into its aggregate representation using the requested functions,
        and custom behaviour if defined on the queryset.
        Returns in a dictionary with results under the key 'data'
        '''
        if 'queryset' in data:
            query_args = self.process_query_params(data.get('request'))

            # TODO: do not raise error here but further down below so we can investigate cause
            try:
                result = self.build_result(data['queryset'], query_args)
            except Exception as e:
                raise AggregateException(str(e))

            data = {'data': result}

            return json.dumps(data, cls=encoders.JSONEncoder)
        return data

    def process_query_params(self, request):
        if not request:
            return {}

        # get the query params we are interested in from the request
        query_args = {
            key: self._clean_agg_query_params(request.query_params, key)
            for key in (_AGGREGATE_KEYWORD, _GROUPBY_KEYWORD)
        }
        return query_args

    def build_result(self, qs, query_args):
        # keys is the list of fields we want to select at the end
        keys = []

        # process group by
        if query_args.get(_GROUPBY_KEYWORD):
            group_keys = []

            # special rules on how to handle fields
            for field in query_args[_GROUPBY_KEYWORD].keys():
                qs, processed_field = self.process_group_by(qs, field)
                group_keys.extend([field, processed_field])

            qs = qs.values(*group_keys).order_by(*group_keys)
            keys.extend(group_keys)

        # process aggregates
        if query_args.get(_AGGREGATE_KEYWORD):
            aggs = {}
            custom_functions = {}

            for fn_name, fn_args in query_args[_AGGREGATE_KEYWORD].items():
                # annotate with the aggregation requested
                for fn_arg in fn_args:
                    try:
                        # aggregate function requested is a default
                        agg_fn = AGGREGATE_FNS[fn_name]
                    except KeyError:
                        # aggregate function requested will be passed on
                        # to the queryset's custom_aggregates method
                        custom_functions[fn_name] = fn_arg
                    else:
                        key = f'{fn_name}_{fn_arg}'.lower()
                        aggs[key] = agg_fn(fn_arg)
                        keys.append(key)

            # if a custom method exists, call it
            # expect it to return a dictionary of aggregate functions
            if hasattr(qs, 'calculate_aggregates'):
                custom_aggs = qs.calculate_aggregates(**custom_functions)
                aggs = {**aggs, **custom_aggs}
                keys.extend(custom_aggs.keys())

            if aggs:
                qs = qs.annotate(**aggs) if query_args.get(_GROUPBY_KEYWORD) else qs.aggregate(**aggs)

        if keys:
            return list(qs.values(*keys)) if not isinstance(qs, dict) else qs
        else:  # if there are no recognised arguments return nothing
            return []

    def process_group_by(self, qs, field):
        '''
        Custom behaviour for field types.
        ChoiceFields will return an additional field with _display that contains the display value
        DateFields have the ability to be grouped by an extracted part (i.e. year, month, day)
        Returns the annotated queryset and field name to be used for the group_by.
        '''
        field_name = field

        # get the django model field definition
        try:
            model_field = qs.model._meta.get_field(field.split('__')[0] if '__' in field else field)
        except FieldDoesNotExist:
            return qs, field_name

        # choices should aslo return the human readable string
        if hasattr(model_field, 'choices') and model_field.choices:
            whens = [
                When(**{field: value, 'then': Value(value_repr)})
                for value, value_repr in model_field.choices
            ]
            field_name = f'{field}_display'
            qs = qs.annotate(**{
                field_name: Case(*whens, default=Value(''), output_field=CharField())
            })

        # extract the date part if requested
        elif issubclass(model_field.__class__, DateField) and '__' in field:
            datefield, part = field.split('__')
            if part == 'date':
                qs = qs.annotate(**{
                    field_name: TruncDate(datefield)
                })
            else:
                qs = qs.annotate(**{
                    field_name: Extract(datefield, part)
                })

        return qs, field_name
