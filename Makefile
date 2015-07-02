ifndef VIRTUAL_ENV
$(warning You should set up a virtualenv.  See the README file.)
endif

test: unittest lint

unittest:
	@nosetests --with-coverage --cover-html --cover-erase --cover-branches --cover-package=loggly

lint:
	@find . -name '*.py' -exec flake8 {} \;

verboselint:
	@find . -name '*.py' -exec flake8 --show-pep8 --show-source {} \;

# remove the doc folder
clean:
	@find . -name "*.pyc" -delete
	@rm -r cover

publish:
	@python setup.py sdist upload

.PHONY: test unittest lint verboselint clean publish 
