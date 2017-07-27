environment:
	virtualenv -p python3 venv; . venv/bin/activate; pip install -r requirements.txt

test:
	python -m unittest discover
