packaging:
	python setup.py sdist

upload:
	twine upload dist/*

dist: clean packaging upload

clean:
	rm -rf dist/