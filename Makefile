DC := $(shell which docker-compose)

.docker-build:
	make build

build:
	${DC} build
	touch .docker-build

run: .docker-build
	${DC} up

shell: .docker-build
	${DC} run web bash

clean:
	rm -rf build/ dist/ .eggs/
	find . -name "*.pyc" -exec rm -f {} +
	rm .docker-build

test: .docker-build
	${DC} run web py.test

.PHONY: build run shell clean
