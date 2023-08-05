# PyTVDB

[![Build Status](https://travis-ci.org/jwbaker/pytvdb.svg?branch=master)](https://travis-ci.org/jwbaker/pytvdb)
[![Coverage Status](https://coveralls.io/repos/github/jwbaker/pytvdb/badge.svg?branch=master)](https://coveralls.io/github/jwbaker/pytvdb?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pytvdb.svg)](https://pypi.python.org/pypi/pytvdb)
[![PyPI](https://img.shields.io/pypi/pyversions/pytvdb.svg)](https://pypi.python.org/pypi/pytvdb)

## Description

PyTVDB is a Python library for querying the TVDB.com API. It was originally written to help me with some personal projects, after I noticed that most existing libraries either:

 - Didn't support Python 3+
 - Hadn't been updated in over a year
 - Used IDE-unfriendly dictionary syntax

So this is my attempt at writing an API library I would actually want to use.

## Supported Python Versions:
PyTVDB supports Python 3.5+.

Python 2.x is not currently supported; support for version 2.7 is planned.

## Requirements
PyTVDB uses the following two libraries:

 - [Requests](http://docs.python-requests.org/en/master/) v2.18.1
 - [TTLDict](https://github.com/mobilityhouse/ttldict) v0.3.0

## Documentation
### Installation
Install using pip:

    pip install pytvdb

### Usage
Start by creating an instance of the ``TVDB`` object:

    from pytvdb import TVDB

    t = TVDB()

If you have an API key on theTVDB.com, you can pass it as an argument:

    t = TVDB(api_key=XXXXXXXX)

From here, the TVDB object exposes fields that mirror the TVDB API routes; for example, to retrieve information for a specific series:

    doctor_who = t.series(76107)

``doctor_who`` now contains series information for [*Doctor Who* (1963)](http://thetvdb.com/?tab=series&id=76107&lid=7)

The following routes are currently implemented:

 - [``/episodes/{id}``](https://api.thetvdb.com/swagger#!/Episodes/get_episodes_id)
 - [``/search/series``](https://api.thetvdb.com/swagger#!/Search/get_search_series)
 - [``/series/{id}``](https://api.thetvdb.com/swagger#!/Series/get_series_id)
 - [``/series/{id}/actors``](https://api.thetvdb.com/swagger#!/Series/get_series_id_actors)
 - [``/series/{id}/episodes``](https://api.thetvdb.com/swagger#!/Series/get_series_episodes)
 - [``/series/{id}/episodes/query``](https://api.thetvdb.com/swagger#!/Series/get_series_id_episodes_query)
 - [``/series/{id}/episodes/summary``](https://api.thetvdb.com/swagger#!/Series/get_series_id_episodes_summary)

## Links

 - [TVDB API documentation](https://api.thetvdb.com/swagger)
