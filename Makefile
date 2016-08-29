PROJECT :=matterpy
GIT_HUB := https://github.com/adfinis-sygroup/matterpy

include pyproject/Makefile

my_custom_pytest: .deps/pytest
   py.test
