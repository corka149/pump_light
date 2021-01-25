# DEVELOPMENT
test:
	pip install -q pytest tox
	tox

format:
	pip install -q autopep8
	autopep8 -r --in-place --aggressive --aggressive --max-line-length 100 src/pump_light

check:
	pip install -q mypy pylint
	mypy src
	pylint src
