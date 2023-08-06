#!/usr/bin/make -f

TEST_ARGS =

all: install test

install:
	virtualenv venv && \
	. venv/bin/activate && \
	pip install -U .

test:
	. venv/bin/activate && \
	registryctl --help && \
	registryctl catalog list
