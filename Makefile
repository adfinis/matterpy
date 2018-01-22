PROJECT :=matterpy
GIT_HUB := https://github.com/adfinis-sygroup/matterpy

DOCKER_PORT := 8080

include pyproject/Makefile

my_custom_pytest: .deps/pytest
	py.test


.PHONY: run-in-docker
run-in-docker:
	docker run --rm -ti -v $(PWD):/code  -w /code -p$(DOCKER_PORT):$(DOCKER_PORT) python:3.5 make _install_and_run

_install_and_run:
	pip install .
	matterpy
