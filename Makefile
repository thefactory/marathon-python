itests:
	tox -e itests

test:
	tox

clean:
	rm -rf dist/ build/

package: clean
	pip install wheel
	python setup.py sdist bdist_wheel

publish: package
	pip install twine
	twine upload dist/*
	github_changelog_generator

.PHONY: itests test clean package publish
