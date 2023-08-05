<h1 align="center">
  <img src="https://raw.githubusercontent.com/Daanvdk/jackster/master/logo_full.png" alt="Jackster"/>
</h1>

[![Build Status](https://travis-ci.org/Daanvdk/jackster.svg?branch=master)](https://travis-ci.org/Daanvdk/jackster)
[![codecov](https://codecov.io/gh/Daanvdk/jackster/branch/master/graph/badge.svg)](https://codecov.io/gh/Daanvdk/jackster)

A python micro webframework focused on keeping your code DRY and short without any black box magic.

## Hello world
Hello world is very short in Jackster, these 3 lines do the trick:
```python
from jackster import Router
from jackster.funcs import html
Router().get(html('Hello world!')).listen()
```

## Install
Jackster is on PyPI, you can install it with:
```
pip install jackster
```
We advise you to do this in a [virtualenv](https://github.com/pypa/virtualenv) for version specific dependency purposes.

## About
Jackster is named after my cat Jack, hence the cat logo.
