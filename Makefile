venv:
	virtualenv -p python3 venv; . venv/bin/activate; pip install -r requirements.txt; deactivate

run:
	. venv/bin/activate; python gun.py; deactivate
