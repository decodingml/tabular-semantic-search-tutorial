install-python:
	uv python install

install:
	uv sync

download-and-process-sample-dataset:
	uv run python -m tools.download_and_process_dataset --data-url https://github.com/shuttie/esci-s/raw/master/sample.json.gz

download-and-process-full-dataset:
	uv run python -m tools.download_and_process_dataset --data-url https://esci-s.s3.amazonaws.com/esci.json.zst

start-superlinked-server:
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
	-d '{"natural_query": "books with a price lower than 100", "limit": 3}' | jq '.'

post-semantic-query:
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/semantic_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "books with a price lower than 100", "limit": 3}' | jq '.'

similar-item-query:
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/semantic_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "similar books to B07WP4RXHY with a rating bigger than 4.5 and a price lower than 100", "limit": 3}' | jq '.'

start-ui:
	uv run streamlit run tools/streamlit_app.py