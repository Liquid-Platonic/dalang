SOURCE=dalang

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr

.PHONY: install
install:
	poetry install

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run


.PHONY: reformat
reformat:
	poetry run isort ${SOURCE}
	poetry run black ${SOURCE}