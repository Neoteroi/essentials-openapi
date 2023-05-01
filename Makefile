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


lint: check-flake8 check-isort check-black


check-flake8:
	@echo "$(BOLD)Checking flake8$(RESET)"
	@flake8 . 2>&1


check-isort:
	@echo "$(BOLD)Checking isort$(RESET)"
	@isort --check-only . 2>&1


check-black:
	@echo "$(BOLD)Checking black$(RESET)"
	@black --check . 2>&1


format:
	@echo "$(BOLD)Formatting code 🧹 🧼$(RESET)"
	@black . 2>&1
	@isort . 2>&1
