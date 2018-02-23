# django-rest-framework-aggregates
[![PyPI version](https://badge.fury.io/py/drf-aggregates.svg)](https://badge.fury.io/py/drf-aggregates) [![Build Status](https://travis-ci.org/uptick/django-rest-framework-aggregates.svg?branch=master)](https://travis-ci.org/uptick/django-rest-framework-aggregates)

Exposes aggregation features of the Django model queryset to the DRF API.

## Requirements

 - Python 3.6+
 - Django 1.11+
 - Django Rest Framework 3.5.3+

## Overview

This renderer overwrites default behaviour for calls made to api v2 .agg endpoints.

Supports `GET` calls to list endpoints in the format:

    endpoint.agg/?aggregate[Count]=(field to count)
    endpoint.agg/?aggregate[Sum]=(field to sum)
    endpoint.agg/?aggregate[custom_function]=arguments
    endpoint.agg/?group_by[field to group by]&aggregate[Count]=id
    endpoint.agg/?group_by[field to group by]&aggregate[Count]=id&aggregate[Sum]=(field to sum)

Supports date part extraction for aggregation:

    endpoint.agg/?group_by[created__year]&aggregate[Count]=id

Supports choices to representation extract:

    endpoint.agg/?group_by[choiceField]&aggregate[Count]=id

## Custom Aggregations

The default aggregate functions supported are defined in `django.db.models.aggregates`.

Custom aggregate functions have been defined in `drf_aggregates.aggregates`

User defined aggregation are passed to a custom queryset manager `calculate_aggregates` as kwargs if defined.

Custom aggregate functions set on the queryset should return a dictionary of field names to aggregate functions, which will then be processed with the other aggregates.

## Examples

Example setup can be found in the [example/](/example/) folder.

To enable the renderer, update your Django settings file:

  ```python
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'drf_aggregates.renderers.AggregateRenderer',
            ...
        ),
        ...
    }
  ```

In the [Cars ViewSet](/example/api/views.py) we are outputting the result to json:

  ```python

      def list(self, request, *args, **kwargs):
          queryset = self.filter_queryset(self.get_queryset())
          data = request.accepted_renderer.render({'queryset': queryset, 'request': request})
          return Response(data, content_type=f'application/json')
  ```


## Tests

In order to run tests locally:

1. Install development requirements:

    `pip3 install -r requirements-dev.txt`

2. Update your environment to point to test Django settings file:

    `export DJANGO_SETTINGS_MODULE=example.settings.test`

3. Run tests:

    `py.test`
