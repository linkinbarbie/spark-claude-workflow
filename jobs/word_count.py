"""Sample PySpark word count job."""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def create_spark_session(app_name: str = "WordCount") -> SparkSession:
    """Create and return a Spark session."""
    return SparkSession.builder.appName(app_name).getOrCreate()


def word_count(spark: SparkSession, text_data: list[str]) -> dict[str, int]:
    """
    Count word occurrences in the given text data.

    Args:
        spark: SparkSession instance
        text_data: List of text strings

    Returns:
        Dictionary mapping words to their counts
    """
    df = spark.createDataFrame([(line,) for line in text_data], ["line"])

    words_df = (
        df.select(F.explode(F.split(F.lower(F.col("line")), r"\s+")).alias("word"))
        .filter(F.col("word") != "")
        .groupBy("word")
        .count()
    )

    return {row["word"]: row["count"] for row in words_df.collect()}


def filter_by_min_count(word_counts: dict[str, int], min_count: int) -> dict[str, int]:
    """Filter words that appear at least min_count times."""
    return {word: count for word, count in word_counts.items() if count >= min_count}
