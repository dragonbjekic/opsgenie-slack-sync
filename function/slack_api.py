from tokenize import group
import slack_sdk
from slack_bolt import App
import logging


class SlackApp:
    def __init__(self, TOKEN):
        self.App = App(token=TOKEN)
        logging.debug(f"slack app created with token {TOKEN}")
        self.groups = self._getGroups()

    def updateGroups(self, mappings):
        for slackGroup in self.groups:
            groupName = slackGroup["name"]
            if groupName in mappings:
                self._updateGroup(slackGroup, mappings[groupName])

    def _getGroups(self):
        groups = []
        for group in self.App.client.usergroups_list()["usergroups"]:
            groups.append(
                {"id": group["id"], "team_id": group["team_id"], "name": group["name"]}
            )
        logging.info("successfully picked up slack groups")
        return groups

    def _updateGroup(self, group, member):
        groupID = group["id"]
        if (
            member == None
        ):  # maybe noone is on-call atm, or the schedule is disabled -> wipe the group
            logging.warn(f"No member found for {groupID}, disabling group")
            try:
                self.App.client.usergroups_disable(usergroup=groupID)
                logging.info(f"group {groupID} disabled")
            except slack_sdk.errors.SlackApiError as e:
                logging.warn(f"error with disabling group: {e}")
        else:
            logging.info(
                f'inserting {member} into {group["name"]}, enabling if previously disabled'
            )
            user = self.App.client.users_lookupByEmail(email=member[0])
            userID = user["user"]["id"]
            logging.debug(f"IDS: user {userID}, group {groupID}")

            try:
                self.App.client.usergroups_enable(usergroup=groupID)
            except slack_sdk.errors.SlackApiError as e:
                logging.warn(f"error with enabling group: ${e}")

            status = self.App.client.usergroups_users_update(
                usergroup=groupID, users=userID
            )
            logging.info(f'group update returned {status["ok"]}')
