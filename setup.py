import re

from setuptools import setup

# Get version this way, so that we don't load any modules.
with open('./drf_aggregates/__init__.py') as f:
    exec(re.search(r'VERSION = .*', f.read(), re.DOTALL).group())

with open('README.md') as file:
    long_description = file.read()

try:
    setup(
        name='drf-aggregates',
        packages=['drf_aggregates'],
        version=__version__,
        description='A Python package that exposes the Django model queryset aggregate functions to the DRF API.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='BSD',
        author='Fiona Lawrence, Jonathan Loo',
        author_email='support@uptickhq.com',
        url='https://github.com/uptick/django-rest-framework-aggregates',
        keywords=['drf', 'django-rest-framework', 'aggregates'],
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Framework :: Django :: 1.11',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Office/Business',
        ],
        install_requires=[],
    )
except NameError:
    raise RuntimeError("Unable to determine version.")
