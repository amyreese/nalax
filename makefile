install:
	python -m pip install -Ue .[dev]

.venv:
	python -m venv .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to activate virtualenv'

venv: .venv

test:
	python -m nalax.tests
	python -m mypy -m nalax

lint:
	python -m flake8 nalax
	python -m ufmt check nalax

format:
	python -m ufmt format nalax

release: lint test clean
	flit publish

clean:
	rm -rf .mypy_cache build dist html *.egg-info

distclean: clean
	rm -rf .venv
