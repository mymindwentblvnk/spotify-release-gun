environment:
	virtualenv -p python3 venv; . venv/bin/activate; pip install -r requirements.txt

test:
	. venv/bin/activate; python -m unittest discover
