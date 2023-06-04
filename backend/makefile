.PHONY: all

venv/bin/activate: requirements.txt
	/usr/local/bin/python3.9 -m venv venv
	./venv/bin/pip install -r requirements.txt

run: venv/bin/activate
	FLASK_APP=src/api.py ./venv/bin/flask run --reload

freeze: venv/bin/pip
	./venv/bin/pip freeze > requirements.txt

clean:
	rm -rf __pycache__
	rm -rf ./env% 