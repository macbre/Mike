coverage_options = --include='mycroft_holmes/*' --omit='test/*'

init:
	pip install -e .[dev]

test:
	pytest -v

lint:
	pylint mycroft_holmes

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m pytest -v
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage xml -i
	coverage report $(coverage_options)

# UI
server_dev:
	FLASK_APP=mycroft_holmes/app/app.py FLASK_ENV=development flask run --host=0.0.0.0

# test database
mysql_cli:
	mysql -h127.0.0.1 -u${TEST_DATABASE_USER} -p${TEST_DATABASE_PASSWORD} ${TEST_DATABASE}

.PHONY: test
