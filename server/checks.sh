isort .
black .
mypy .

rm tests.db
DB_FILE="tests.db" pytest .
DB_FILE="tests.db" pytest test.py
