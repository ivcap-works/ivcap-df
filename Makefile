
# Git information
GIT_COMMIT := $(shell git rev-parse --short HEAD)
GIT_REPOSITORY := $(shell git config --get remote.origin.url)
GIT_TAG := $(shell git describe --abbrev=0 --tags ${GIT_COMMIT} 2>/dev/null || true)

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

build:
	poetry build

test:
	pytest ${ROOT_DIR}/tests/

clean:
	rm -rf *.egg-info
	rm -rf dist
	find ${ROOT_DIR} -name __pycache__ | xargs rm -r 
