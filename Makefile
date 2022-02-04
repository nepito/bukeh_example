myapp/salidita.html: myapp/secod_try.py
	python myapp/secod_try.py > myapp/salidita.html

check:
	black --check --line-length 100 myapp
	flake8 --max-line-length 100 myapp

deploy:
	ansible-playbook -u root -i 143.198.228.215, --private-key "~/.ssh/id_rsa" playbook.yml

format:
	black --line-length 100 myapp

run:
	bokeh serve --show --port=3535 myapp/main.py