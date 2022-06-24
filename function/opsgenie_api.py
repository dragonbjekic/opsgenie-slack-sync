import logging
import json
import requests


def getSchedules(APIKEY):
    request_url = "https://api.opsgenie.com/v2/schedules/"
    headers = {"Authorization": "GenieKey " + APIKEY}

    req = requests.get(request_url, headers=headers)
    reqData = req.json()["data"]

    schedules = []

    for schedule in reqData:
        schedules.append(schedule["name"])

    return schedules


def populateWithEmails(mappings, APIKEY):
    schedules = getSchedules(APIKEY)

    updatedMappings = {}

    for slackGroup in mappings:
        ogSchedule = mappings[slackGroup]
        if ogSchedule in schedules:
            updatedMappings[slackGroup] = whosOnCall(ogSchedule, APIKEY)
        else:
            updatedMappings[slackGroup] = None
            logging.warn(
                f"no schedule named {ogSchedule} found for slack group {slackGroup}"
            )

    return updatedMappings


def whosOnCall(schedule, APIKEY):
    logging.debug(f"using {APIKEY} for opsgenie requests")

    request_url = f"https://api.opsgenie.com/v2/schedules/{schedule}/on-calls"
    headers = {"Authorization": f"GenieKey {APIKEY}"}
    params = {"scheduleIdentifierType": "name", "flat": "true"}

    req = requests.get(request_url, params=params, headers=headers)

    reqData = req.json()["data"]
    logging.debug(reqData)

    if len(reqData["onCallRecipients"]) != 0 and reqData["_parent"]["enabled"]:
        logging.info(f'oncall for {schedule}: {reqData["onCallRecipients"]}')
        return reqData["onCallRecipients"]
    else:
        logging.warn(f"Schedule {schedule} is currently disabled")
        return None
