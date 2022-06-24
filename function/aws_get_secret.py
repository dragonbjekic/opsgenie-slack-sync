import json
import logging
import boto3


def get_secret(secret_arn):
    aws_sm_client = boto3.client("secretsmanager")
    my_secret = aws_sm_client.get_secret_value(SecretId=secret_arn).get("SecretString")
    logging.info("successfully obtained secret")
    return my_secret
