myapp/salidita.html: myapp/secod_try.py
	python myapp/secod_try.py > myapp/salidita.html

.PHONY: init install tests

build:
	docker build --tag=mamando .

buildConPandas:
	docker build --tag=con-pandas -f Dockerfile-dev .

check:
	black --check --line-length 100 myapp
	flake8 --max-line-length 100 myapp
	black --check --line-length 100 src
	flake8 --max-line-length 100 src
	black --check --line-length 100 tests
	flake8 --max-line-length 100 tests
	black --check --line-length 100 xg_plots
	flake8 --max-line-length 100 xg_plots

deploy:
	ansible-playbook -u root -i 143.198.228.215, --private-key "~/.ssh/id_rsa" playbook.yml

format:
	black --line-length 100 myapp
	black --line-length 100 src
	black --line-length 100 tests
	black --line-length 100 xg_plots

init: install tests

install:
	pip install --editable .

run:
	bokeh serve --show --port=3535 myapp/main.py

up:
	docker run --detach --publish=3535:3535 mamando make run
	
update_note: trimestre_por_estudios.csv
	docker run -v $PWD/myapp/:/myapp/myapp con-pandas make myapp/salidita.html

trimestre_por_estudios.csv:
	Rscript src/clean_data.R

tests:
	pytest --verbose