.PHONY: release test annotate


test-debug:
	rm debug* && DEBUG=1 pytest tests/test_v3.py


artifacts: test
	python setup.py sdist


prepforbuild:
	pip install --upgrade twine setuptools wheel


testrelease:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


release: artifacts
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


test:
	pytest tests/


init:
	pip install -r requirements.txt


test-v:
	pytest -v


test-cov-unit:
	pytest --cov-report html --cov=openapidocs tests


test-cov:
	pytest --cov-report html --cov=openapidocs
