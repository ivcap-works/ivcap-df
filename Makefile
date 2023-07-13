
# Git information
GIT_COMMIT := $(shell git rev-parse --short HEAD)
GIT_REPOSITORY := $(shell git config --get remote.origin.url)
GIT_TAG := $(shell git describe --abbrev=0 --tags ${GIT_COMMIT} 2>/dev/null || true)

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

build: add-license
	poetry build

test:
	poetry run pytest tests/ --cov=ivcap_df --cov-report=xml

docs:
	rm -rf ${ROOT_DIR}/docs/_build
	cd ${ROOT_DIR}/docs && make html

add-license:
	licenseheaders -t .license.tmpl -y 2023 -d src
	licenseheaders -t .license.tmpl -y 2023 -d examples

clean:
	rm -rf *.egg-info
	rm -rf dist
	find ${ROOT_DIR} -name __pycache__ | xargs rm -r 

.PHONY: docs
