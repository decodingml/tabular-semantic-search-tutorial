import superlinked.framework as sl

from product_search import index, query
from product_search.config import settings

product_source: sl.RestSource = sl.RestSource(index.product)

product_data_loader_parser = sl.DataFrameParser(
    schema=index.product, mapping={index.product.id: "asin"}
)
product_data_loader_config = sl.DataLoaderConfig(
    "./data/processed_samples.jsonl",
    sl.DataFormat.JSON,
    pandas_read_kwargs={"lines": True, "chunksize": 100},
)
product_loader_source: sl.DataLoaderSource = sl.DataLoaderSource(
    index.product,
    data_loader_config=product_data_loader_config,
    parser=product_data_loader_parser,
)

if settings.USE_MONGODB:
    vector_database = sl.MongoDBVectorDatabase(
        settings.MONGO_CLUSTER_URL,
        settings.MONGO_DATABASE_NAME,
        settings.MONGO_CLUSTER_NAME,
        settings.MONGO_PROJECT_ID,
        settings.MONGO_API_PUBLIC_KEY,
        settings.MONGO_API_PRIVATE_KEY,
    )
else:
    vector_database = vector_database = sl.InMemoryVectorDatabase()

executor = sl.RestExecutor(
    sources=[product_source, product_loader_source],
    indices=[index.product_index],
    queries=[
        sl.RestQuery(sl.RestDescriptor("filter_query"), query.filter_query),
        sl.RestQuery(sl.RestDescriptor("semantic_query"), query.semantic_query),
        sl.RestQuery(
            sl.RestDescriptor("similar_items_query"), query.similar_items_query
        ),
    ],
    vector_database=vector_database,
)

sl.SuperlinkedRegistry.register(executor)
