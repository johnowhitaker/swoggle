SRC = $(wildcard ./*.ipynb)
DIST := python setup.py sdist bdist_wheel

all: swoggle docs

swoggle: $(SRC)
	nbdev_build_lib
	touch swoggle

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: bump clean
	$(DIST)
	twine upload --repository pypi dist/*

pypi: dist
	twine upload --repository pypi dist/*

bump:
	nbdev_bump_version

dist: clean
	$(DIST)

clean:
	rm -rf dist