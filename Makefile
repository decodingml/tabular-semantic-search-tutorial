install-python:
	uv python install

install:
	uv sync

start-server:
	uv run python -m superlinked.server

load-data:
	curl -X 'POST' \
	'http://localhost:8080/data-loader/product_schema/run' \
	-H 'accept: application/json' \
	-d ''

post-filter-query:
	curl -X POST \
	'http://localhost:8080/api/v1/search/filter_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "books with a price lower than 100"}'