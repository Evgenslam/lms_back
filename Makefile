.PHONY: fm

f = .

fm:
	isort ${f} && autoflake --remove-all-unused-imports --in-place ${f}