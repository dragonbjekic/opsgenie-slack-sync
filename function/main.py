import logging
import os
import json
import configparser
from slack_api import SlackApp
import opsgenie_api as og
import aws_get_secret


def local():
    # local testing
    with open("./apikeys", "r") as apiKeysFile:
        apiKeys = json.load(apiKeysFile)
    SLACK_API_TOKEN = apiKeys["slack"]
    OPSGENIE_API_TOKEN = apiKeys["opsgenie"]
    return SLACK_API_TOKEN, OPSGENIE_API_TOKEN


def handler(event="", context=""):
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    if logging.getLogger().hasHandlers():
        print("has")
        logging.getLogger().setLevel(loglevel)
    else:
        print("hasn't")
        logging.basicConfig(level=loglevel)

    response = {
        "statusCode": 200,
        "body": "Execution finished. Check CloudWatch Logs for more info",
    }

    # local testing
    # SLACK_API_TOKEN, OPSGENIE_API_TOKEN = local()

    secret_arn = os.environ.get("SECRET_ARN")
    apiKeysString = aws_get_secret.get_secret(secret_arn)
    apiKeys = json.loads(apiKeysString)
    SLACK_API_TOKEN = apiKeys["slack"]
    OPSGENIE_API_TOKEN = apiKeys["opsgenie"]

    mappingsFile = configparser.ConfigParser()
    mappingsFile.read("./mappings.ini")
    mappings = mappingsFile["mappings"]
    logging.info("loaded mappings")

    slackApp = SlackApp(SLACK_API_TOKEN)
    updatedMappings = og.populateWithEmails(mappings, OPSGENIE_API_TOKEN)
    logging.debug(f"Updated Mappings: \n {updatedMappings}")

    slackApp.updateGroups(updatedMappings)

    logging.info("Execution completed successfully")
    return response


# for local testing
if __name__ == "__main__":
    handler()
