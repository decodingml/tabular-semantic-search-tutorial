from urllib.parse import urlparse, urlunparse

from loguru import logger
from pymongo.mongo_client import MongoClient

from superlinked_app.config import settings

assert (
    settings.MONGO_CLUSTER_URL
), "MONGO_CLUSTER_URL must be set in environment variables"
assert (
    settings.MONGO_DATABASE_NAME
), "MONGO_DATABASE_NAME must be set in environment variables"


uri = (
    f"mongodb+srv://{settings.MONGO_CLUSTER_URL}"
    if "mongodb+srv://" not in settings.MONGO_CLUSTER_URL
    else f"{settings.MONGO_CLUSTER_URL}"
)
logger.info(f"Loading to Mongo with '{uri}'")
client = MongoClient(uri)


def create_database(database_name: str) -> bool:
    logger.info(f"Creating database '{database_name}'")
    try:
        # Create database by creating and then dropping a temporary collection
        db = client[database_name]
        temp_collection = "temp_initialization_collection"
        db.create_collection(temp_collection)

        logger.info(f"Successfully created database '{database_name}'")

        return True
    except Exception as e:
        logger.error(f"Error creating database: {e}")

        return False
    finally:
        client.close()


if __name__ == "__main__":
    create_database(settings.MONGO_DATABASE_NAME)
