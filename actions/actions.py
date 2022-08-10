
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import requests

class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_greet_user")

        return [UserUtteranceReverted()]


class ActionCorona(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://api.covid19india.org/data.json").json()

        entitites = tracker.latest_message['entities']
        print("message", entitites)
        state = None

        for e in entitites:
            if e['entity'] == 'state':
                state = e['value']

        message = "please enter correct state"
        if state == "india":
            state = "total"

        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Active: " + data["active"] + "\n Confirmed: " + data["confirmed"]+"\n Recovered:  " + data["recovered"]
                mess = "\n state notes:  " + data["statenotes"]

        print(message)
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text=mess)

        return []


