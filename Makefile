check:
	ty check project/
check-format:
	ruff format --diff project/
format:
	ruff format project/
lint:
	ruff check project/
lint-fix:
	ruff check --fix project/

.PHONY: check check-format format lint lint-fix
