
test::
	pytest tests/test*.py
	pytest tests/tests_class_flexdatetime
	pytest tests/tests_flex_datetime
	pytest tests/tests_flex_time

format::
	toml-sort pyproject.toml

build:: format
	uv build

publish:: build
	uv publish