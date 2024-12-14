import superlinked.framework as sl
from loguru import logger

from superlinked_app import index, query
from superlinked_app.config import settings

# Define the real-time data loader (takes items one by one through HTTP requests).
product_source: sl.RestSource = sl.RestSource(index.product)

# Define the batch data loader (loads our static dataset).
logger.info(f"Data loader will load data from: '{settings.PROCESSED_DATASET_PATH}'")
settings.validate_processed_dataset_exists()
product_data_loader_parser = sl.DataFrameParser(
    schema=index.product, mapping={index.product.id: "asin"}
)
product_data_loader_config = sl.DataLoaderConfig(
    str(settings.PROCESSED_DATASET_PATH),
    sl.DataFormat.JSON,
    pandas_read_kwargs={"lines": True, "chunksize": 100},
)
product_loader_source: sl.DataLoaderSource = sl.DataLoaderSource(
    index.product,
    data_loader_config=product_data_loader_config,
    parser=product_data_loader_parser,
)

if settings.USE_MONGO_VECTOR_DB:
    logger.info("Using MongoDBVectorDatabase as your vector database.")
    vector_database = sl.MongoDBVectorDatabase(
        settings.MONGO_CLUSTER_URL,
        settings.MONGO_DATABASE_NAME,
        settings.MONGO_CLUSTER_NAME,
        settings.MONGO_PROJECT_ID,
        settings.MONGO_API_PUBLIC_KEY,
        settings.MONGO_API_PRIVATE_KEY,
    )
else:
    logger.info("Using InMemoryVectorDatabase as your vector database.")
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
