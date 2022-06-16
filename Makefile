myapp/salidita.html: myapp/secod_try.py
	python myapp/secod_try.py > myapp/salidita.html

build:
	docker build --tag=mamando .

buildConPandas:
	docker build --tag=con-pandas -f Dockerfile-dev .

check:
	black --check --line-length 100 myapp
	flake8 --max-line-length 100 myapp

deploy:
	ansible-playbook -u root -i 143.198.228.215, --private-key "~/.ssh/id_rsa" playbook.yml

format:
	black --line-length 100 myapp

run:
	bokeh serve --show --port=3535 myapp/main.py

up:
	docker run --detach --publish=3535:3535 mamando make run
	
update_note: trimestre_por_estudios.csv
	docker run -v $PWD/myapp/:/myapp/myapp con-pandas make myapp/salidita.html

trimestre_por_estudios.csv:
	Rscript src/clean_data.R