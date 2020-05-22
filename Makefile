itests: itests-py36 itests-py37

itests-py36:
	tox -e itest-py36

itests-py37:
	tox -e itest-py37

test: test-py36 test-py37

test-py36:
	tox -e pep8
	tox -e test-py36

test-py37:
	tox -e test-py37

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
