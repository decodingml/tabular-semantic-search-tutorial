import random
from typing import Optional

import pandas as pd


def parse_category(category: str) -> list[str]:
    """Parse the category string and return the first category.

    Args:
        category: String containing the category list (e.g., "['Books', 'Fiction', 'Literature']")

    Returns:
        String containing the first category, or None if parsing fails
    """
    if isinstance(category, list) and pd.isna(category).any():
        return []
    elif not isinstance(category, list) and pd.isna(category):
        return []

    try:
        keep_num_categories = 1 if random.random() < 0.9 else 2
        return [c.strip() for c in category][:keep_num_categories]
    except (ValueError, IndexError):
        return []


def parse_review_rating(stars: str) -> Optional[float]:
    """Parse the stars rating from a string to a float value between 0 and 5.

    Args:
        stars: String containing the star rating (e.g., "4.2 out of 5 stars", "4,2 de 5 estrellas")

    Returns:
        Float value between 0 and 5, or None if parsing fails
    """

    if pd.isna(stars):
        return -1.0
    stars_str = str(stars).replace(",", ".")  # Handle European number format
    try:
        return float(stars_str.split()[0])
    except (ValueError, IndexError):
        return -1.0


def parse_review_count(ratings: str) -> Optional[int]:
    """Parse the number of ratings from a string to a float value.

    Args:
        ratings: String containing the number of ratings (e.g., "1,116 ratings", "90 valoraciones")

    Returns:
        Int value representing the number of ratings, or None if parsing fails
    """

    if pd.isna(ratings):
        return 0
    try:
        # Remove commas and get first number
        ratings_str = str(ratings).split()[0].replace(",.", "")
        return int(ratings_str)
    except (ValueError, IndexError):
        return 0


def parse_price(price: str) -> Optional[float]:
    """Parse the price from a string to a float value.

    Args:
        price: String containing the price (e.g., "$9.99", "25,63€")

    Returns:
        Float value representing the price, or -10 if parsing fails or price is NaN
    """
    if pd.isna(price):
        return None

    try:
        # Remove currency symbols and convert to float
        price_str = str(price).replace("$", "").replace("€", "").replace(",", ".")
        return min(float(price_str), 1000.0)
    except ValueError:
        return None


def process_amazon_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Process raw product data into a standardized format.

    This function takes a DataFrame containing raw product data and processes it to ensure
    consistent data types and formats across all fields.

    Args:
        df: Input DataFrame containing raw product data with columns:
            - asin (str): Amazon Standard Identification Number
            - type (str): Product type
            - title (str): Product title
            - description (str): Product description
            - stars (str): Star rating
            - ratings (str): Number of ratings
            - price (str): Product price

    Returns:
        Processed DataFrame with the following columns and types:
            - asin (str): Unchanged
            - type (str): Unchanged
            - title (str): Unchanged
            - description (str): Unchanged
            - review_rating (float): Value between 0 and 5
            - review_count (float): Number of ratings
            - price (float): Price value
    """

    random.seed(6)

    # Create a copy to avoid modifying the original DataFrame
    df_processed = df.copy()
    df_processed = df_processed[df_processed["locale"] == "us"]

    # Keep only required columns
    columns_to_keep = [
        "asin",
        "type",
        "category",
        "title",
        "description",
        "stars",
        "ratings",
        "price",
    ]
    df_processed = df_processed[columns_to_keep]

    # Apply transformations
    df_processed["category"] = df_processed["category"].apply(parse_category)
    df_processed["review_rating"] = df_processed["stars"].apply(parse_review_rating)
    df_processed["review_count"] = df_processed["ratings"].apply(parse_review_count)
    df_processed["price"] = df_processed["price"].apply(parse_price)

    # Drop original stars and ratings columns since we've extracted the values
    df_processed = df_processed.drop(columns=["stars", "ratings"])

    df_processed = df_processed.dropna(
        subset=["price"]
    ).astype(
        {
            "asin": str,
            "type": str,
            "title": str,
            "description": str,
            "review_rating": float,
            "review_count": int,
            "price": float,
        }
    )

    return df_processed
