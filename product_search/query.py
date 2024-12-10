from superlinked import framework as sl

from product_search import index
from product_search.config import settings

assert (
    settings.OPENAI_API_KEY
), "OPENAI_API_KEY must be set in environment variables to use natural language queries"


# fill this with your API key - this will drive param extraction
openai_config = sl.OpenAIClientConfig(
    api_key=settings.OPENAI_API_KEY.get_secret_value(), model=settings.OPENAI_MODEL_ID
)

text_similar_param = sl.Param(
    "query_text",
    description=(
        "The text in the user's query that is used to search in the products' description."
        " Extract info that does not apply to other spaces or params."
    ),
)
price_param = sl.Param(
    "query_price",
    description=(
        "The text in the user's query that is used to search based on the products price."
        " Extract info that does not apply to other spaces or params."
    ),
)
review_rating_param = sl.Param(
    "query_review_rating",
    description=(
        "The text in the user's query that is used to search based on the products review rating."
        " Extract info that does not apply to other spaces or params."
    ),
)

# Define your query using dynamic parameters for query text and weights.
# let's create a base query that we will modify to 2 alternative versions
base_query = (
    sl.Query(
        index.product_index,
        weights={
            index.description_space: sl.Param("description_weight"),
            index.review_rating_maximizer_space: sl.Param("stars_maximizer_weight"),
            index.price_minimizer_space: sl.Param("price_minimizer_weights"),
        },
    )
    .find(index.product)
    .limit(sl.Param("limit"))
    # we will have our LLM fill them based on our natural language query
    .with_natural_query(sl.Param("natural_query"), openai_config)
    .filter(
        index.product.type
        == sl.Param(
            "filter_by_type",
            description="Used to only present items that have a specific type",
            options=["product", "book"],
        )
    )
)

filter_query = (
    base_query.similar(
        index.description_space,
        text_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .filter(
        index.product.review_rating
        >= sl.Param(
            "rating_bigger_than",
            description="Used to find items with a rating bigger than the provided number.",
        )
    )
    .filter(
        index.product.price
        <= sl.Param(
            "price_smaller_than",
            description="Used to find items with a price smaller than the provided number.",
        )
    )
)

semantic_query = (
    base_query.similar(
        index.description_space,
        text_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .similar(
        index.price_minimizer_space,
        price_param,
        sl.Param("price_similar_clause_weight"),
    )
    .similar(
        index.review_rating_maximizer_space,
        review_rating_param,
        sl.Param("review_rating_similar_clause_weight"),
    )
)

similar_items_query = filter_query.with_vector(index.product, sl.Param("product_id"))
