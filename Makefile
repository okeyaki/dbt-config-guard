.PHONY: build
build:
	@uv build

.PHONY: format
format:
	@ruff check --fix src/

.PHONY: lint
lint:
	mypy src/

.PHONY: generate
generate:
	@uv run bin/generate.py

.PHONY: test
test:
	@pytest --cov

.PHONY: publish-test
publish-test: build
	@uv publish --publish-url https://test.pypi.org/legacy/
