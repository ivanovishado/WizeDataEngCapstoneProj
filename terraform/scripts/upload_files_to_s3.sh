#!/usr/bin/env bash

aws s3 cp ../../dags/scripts/spark/random_text_classification.py \
    $(terraform output -raw s3_id_spark)/scripts/random_text_classification.py

aws s3 cp ../../dags/scripts/spark/user_behavior_metrics.py \
    $(terraform output -raw s3_id_spark)/scripts/user_behavior_metrics.py

unzip -o ../../data/movie_review.zip

aws s3 cp ../../data/movie_review.csv \
    $(terraform output -raw s3_id_raw)/data/movie_review.csv
