import argparse

from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.sql.functions import array_contains, col


def random_text_classifier(input_loc, output_loc):
    """
    This is a function to naively classify movie reviews as good or bad,
    depending on the existence of the word "good" in the review.

    Other approaches could be made to have a more robust classification,
    such as a model that has been trained with millions of reviews.
    """

    df_raw = spark.read.option("header", True).csv(input_loc)

    tokenizer = Tokenizer(inputCol="review_str", outputCol="review_token")
    df_tokens = tokenizer.transform(df_raw).select("cid", "review_token")

    remover = StopWordsRemover(inputCol="review_token", outputCol="review_clean")
    df_clean = remover.transform(df_tokens).select("cid", "review_clean")

    df_out = df_clean.select(
        "cid", array_contains(df_clean.review_clean, "good").alias("positive_review")
    )

    df_res = df_out.select(col("positive_review").cast("integer"))

    df_res.write.mode("overwrite").parquet(output_loc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="HDFS input", default="/movie")
    parser.add_argument("--output", type=str, help="HDFS output", default="/output")
    args = parser.parse_args()
    spark = SparkSession.builder.appName("Random Text Classifier").getOrCreate()
    random_text_classifier(input_loc=args.input, output_loc=args.output)
