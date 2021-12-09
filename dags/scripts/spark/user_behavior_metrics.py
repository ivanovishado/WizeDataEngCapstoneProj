import argparse

from datetime import datetime

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    regexp_replace,
    lit,
    format_number,
    to_timestamp,
)
from pyspark.sql.types import DoubleType, IntegerType


def calculate_user_behavior_metrics(
    reviews_loc, purchases_loc, insert_date, output_loc
):
    """
    This is a function to calculate user behavior metrics
    based on user's movie reviews and purchases.
    """

    movie_reviews = spark.read.parquet(reviews_loc)

    movie_reviews = movie_reviews.groupby("cid").agg(
        F.count("positive_review").alias("review_count"),
        F.sum("positive_review").alias("review_score"),
    )

    user_purchases = spark.read.option("header", True).csv(purchases_loc)

    user_purchases = user_purchases.withColumn(
        "amount_spent", user_purchases["Quantity"] * user_purchases["UnitPrice"]
    )

    user_purchases = user_purchases.groupBy("CustomerID").agg(
        F.sum(user_purchases.amount_spent).alias("sum")
    )

    user_purchases = user_purchases.withColumn(
        "amount_spent", format_number(user_purchases.sum, 2)
    ).drop("sum")
    user_purchases = user_purchases.withColumn(
        "amount_spent", regexp_replace(user_purchases.amount_spent, ",", "")
    )

    # Probably can be parsed to a float. Need to check the data.
    user_purchases = user_purchases.withColumn(
        "amount_spent", user_purchases["amount_spent"].cast(DoubleType())
    )

    joined_dfs = user_purchases.join(
        movie_reviews, movie_reviews.cid == user_purchases.CustomerID
    ).drop("cid")
    joined_dfs = joined_dfs.withColumn(
        "CustomerID", joined_dfs["CustomerID"].cast(IntegerType())
    )
    joined_dfs = joined_dfs.withColumn(
        "review_count", joined_dfs["review_count"].cast(IntegerType())
    )
    joined_dfs = joined_dfs.withColumn(
        "review_score", joined_dfs["review_score"].cast(IntegerType())
    )

    joined_dfs = joined_dfs.withColumn(
        "insert_date",
        to_timestamp(lit(insert_date)),
    )

    joined_dfs.write.mode("overwrite").parquet(output_loc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--purchases",
        type=str,
        help="User purchases filepath",
        default="/purchases",
    )
    parser.add_argument(
        "--reviews", type=str, help="Movie reviews filepath", default="/reviews"
    )
    parser.add_argument("--date", type=str, help="Date", default=datetime.now())
    parser.add_argument("--output", type=str, help="Output", default="/output")

    args = parser.parse_args()

    spark = SparkSession.builder.appName(
        "User Behavior Metrics Calculator"
    ).getOrCreate()

    calculate_user_behavior_metrics(
        purchases_loc=args.purchases,
        reviews_loc=args.reviews,
        insert_date=args.date,
        output_loc=args.output,
    )
