itests:
	tox -e itest-py27,itest-py33

test:
	tox -e pep8,test-py27,test-py33

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
