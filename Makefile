.PHONY: release test annotate


test-debug:
	rm debug* && DEBUG=1 pytest tests/test_v3.py


artifacts: test
	python -m build


prepforbuild:
	pip install build


build:
	python -m build


test-release:
	twine upload --repository testpypi dist/*


release:
	twine upload --repository pypi dist/*


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


format:
	isort openapidocs
	isort tests
	black openapidocs
	black tests
