check:
	black --check --line-length 100 myapp
	flake8 --max-line-length 100 myapp

format:
	black --line-length 100 myapp

run:
	bokeh serve --show myapp/main.py