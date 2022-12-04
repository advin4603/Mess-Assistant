# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from datetime import datetime
import calendar
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from .menu import menu
from bs4 import BeautifulSoup
import bs4
import requests

MESS_URL = "https://mess.iiit.ac.in/mess/web/student_home.php"
MESS_VIEW_URL = "https://mess.iiit.ac.in/mess/web/student_view_registration.php"


class ActionSessionIdCheck(Action):
    def name(self) -> Text:
        return "action_session_id_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        session_id, tgc = tracker.get_slot('session_id').strip("_").split("|")
        print(session_id)
        print(tgc)
        result = requests.get(MESS_URL, cookies={"PHPSESSID": session_id, "TGC": tgc})
        result_soup = BeautifulSoup(result.content)
        title = result_soup.select_one("title").contents
        print(title)
        if title and title[0] == "Student Home":
            dispatcher.utter_message(json_message={"data": {"verified": True}})
            return []
        dispatcher.utter_message(json_message={"data": {"verified": False}})
        return [SlotSet("session_id", None)]


class ActionSubmitMealChange(Action):
    def name(self) -> Text:
        return "submit_meal_change"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Ok I am changing your meal")
        messes = tracker.get_slot("mess")
        dates = tracker.get_slot("time")
        times = tracker.get_slot("meal_time")
        print("", messes, dates, times, sep="\n\t")
        return [SlotSet("time", None), SlotSet("meal_time", None), SlotSet("mess", None)]


class ActionSubmitMealCancel(Action):
    def name(self) -> Text:
        return "submit_meal_cancel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Ok I am cancelling your meal")
        dates = tracker.get_slot("time")
        times = tracker.get_slot("meal_time")
        print("", dates, times, sep="\n\t")
        return [SlotSet("time", None), SlotSet("meal_time", None)]


class ActionSubmitMealUncancel(Action):
    def name(self) -> Text:
        return "submit_meal_uncancel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Ok I am uncancelling your meal")
        dates = tracker.get_slot("time")
        times = tracker.get_slot("meal_time")
        print("", dates, times, sep="\n\t")
        return [SlotSet("time", None), SlotSet("meal_time", None)]


class ValidateMealCancelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_meal_cancel_form"

    def validate_meal_time(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value not in ("breakfast", "lunch", "dinner", "all meals"):
            dispatcher.utter_message(f"{slot_value} is an invalid meal.")
            return {"meal_time": None}
        return {"meal_time": slot_value}

    def validate_time(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if type(slot_value) == str:
            time_obj = datetime.fromisoformat(slot_value)
            delta = time_obj - datetime.now()
            if delta.days < 2:
                dispatcher.utter_message("You can only cancel your mess from atleast two days in advance.")
                return {"time": None}
            return {"time": slot_value}
        if type(slot_value) == dict and "from" in slot_value and "to" in slot_value:
            time_obj = datetime.fromisoformat(slot_value)
            delta = time_obj - datetime.now()
            if delta.days < 2:
                dispatcher.utter_message("You can only cancel your mess from atleast two days in advance.")
                return {"time": None}
            return {"time": slot_value}
        dispatcher.utter_message(f"{slot_value} is an invalid time.")
        return {"time": None}


class ValidateMealUncancelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_meal_uncancel_form"

    def validate_meal_time(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value not in ("breakfast", "lunch", "dinner", "all meals"):
            dispatcher.utter_message(f"{slot_value} is an invalid meal.")
            return {"meal_time": None}
        return {"meal_time": slot_value}

    def validate_time(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if type(slot_value) == str:
            time_obj = datetime.fromisoformat(slot_value)
            delta = time_obj - datetime.now()
            if delta.days < 2:
                dispatcher.utter_message("You can only uncancel your mess from atleast two days in advance.")
                return {"time": None}
            return {"time": slot_value}
        if type(slot_value) == dict and "from" in slot_value and "to" in slot_value:
            time_obj = datetime.fromisoformat(slot_value)
            delta = time_obj - datetime.now()
            if delta.days < 2:
                dispatcher.utter_message("You can only uncancel your mess from atleast two days in advance.")
                return {"time": None}
            return {"time": slot_value}
        dispatcher.utter_message(f"{slot_value} is an invalid time.")
        return {"time": None}


class ValidateMealChangeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_meal_change_form"

    def validate_meal_time(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value not in ("breakfast", "lunch", "dinner", "all meals"):
            dispatcher.utter_message(f"{slot_value} is an invalid meal.")
            return {"meal_time": None}
        return {"meal_time": slot_value}

    def validate_time(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if type(slot_value) == str:
            time_obj = datetime.fromisoformat(slot_value)
            delta = time_obj - datetime.now()
            if delta.days < 2:
                dispatcher.utter_message("You can only change your mess from atleast two days in advance.")
                return {"time": None}
            return {"time": slot_value}
        if type(slot_value) == dict and "from" in slot_value and "to" in slot_value:
            time_obj = datetime.fromisoformat(slot_value)
            delta = time_obj - datetime.now()
            if delta.days < 2:
                dispatcher.utter_message("You can only change your mess from atleast two days in advance.")
                return {"time": None}
            return {"time": slot_value}
        dispatcher.utter_message(f"{slot_value} is an invalid time.")
        return {"time": None}

    def validate_mess(self, slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: DomainDict,
                      ) -> Dict[Text, Any]:
        if slot_value not in mess_name_transform.values():
            dispatcher.utter_message(text=f"{slot_value} is not a valid mess")
            return {"mess": None}


mess_name_transform = {
    "Kadamb-Veg": "kadamba veg mess",
    "North": "north mess",
    "South": "south mess",
    "Yuktahaar": "yuktahar mess",
    "Kadamb Non-Veg": "kadamba non veg mess"
}


class ActionMenuCheck(Action):

    def name(self) -> Text:
        return "action_menu_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        messes = list(tracker.get_latest_entity_values("mess"))
        dates = list(tracker.get_latest_entity_values("time"))
        times = list(tracker.get_latest_entity_values("meal_time"))
        print(dates)
        if dates:
            if type(dates[0]) == str:
                date = datetime.fromisoformat(dates[0])
            else:
                # ignore type mismatch
                date = datetime.fromisoformat(dates[0]["to"])
        else:
            date = datetime.now()

        if times:
            time = times[0]
        else:
            time = "all meals"
        print(time)
        if time == "all meals":
            mess = "north mess", "north mess", "north mess"
        else:
            mess = "north mess"

        if messes:
            mess = messes[0]
        else:
            ssid = tracker.get_slot('session_id')
            if ssid is None:
                dispatcher.utter_message("You are not authenticated, so im checking North Mess' Menu")
            else:
                session_id, tgc = ssid.strip("_").split("|")
                result = requests.get(MESS_VIEW_URL, {"month": date.month, "year": date.year},
                                      cookies={"PHPSESSID": session_id, "TGC": tgc})
                result_soup = BeautifulSoup(result.content)

                for td in result_soup.select(".linked-day"):
                    if type(td.contents[0].contents[0]) == bs4.element.NavigableString:
                        date_num = int(td.contents[0].contents[0])
                    else:
                        date_num = int(td.contents[0].contents[0].contents[0])
                    if date_num == date.day:
                        if len(td.contents) == 7:
                            if time == "breakfast":
                                mess = str(td.contents[2])[:-3]
                            elif time == "lunch":
                                mess = str(td.contents[4])[:-3]
                            elif time == "dinner":
                                mess = str(td.contents[6])[:-3]
                            elif time == "all meals":
                                mess = str(td.contents[2])[:-3], str(td.contents[4])[:-3], str(td.contents[6])[:-3]
                        else:
                            if time == "breakfast":
                                mess = str(td.contents[1].contents[0].contents[-1])[:-3]
                            elif time == "lunch":
                                mess = str(td.contents[2].contents[0].contents[-1])[:-3]
                            elif time == "dinner":
                                mess = str(td.contents[3].contents[0].contents[-1])[:-3]
                            elif time == "all meals":
                                mess = str(td.contents[1].contents[0].contents[-1])[:-3], str(
                                    td.contents[2].contents[0].contents[-1])[:-3], str(
                                    td.contents[3].contents[0].contents[-1])[:-3]
                        if time == "all meals":
                            mess = [mess_name_transform[m] for m in mess]
                        else:
                            mess = mess_name_transform[mess]
        date = calendar.day_name[date.weekday()].lower()

        if time == "all meals":
            for t, m in zip(("breakfast", "lunch", "dinner"), mess):
                try:
                    meal = menu[date][m][t]
                except KeyError:
                    dispatcher.utter_message(text=f"{m} does not serve anything for {date} {t}.")
                else:
                    dispatcher.utter_message(text=f"{m} is serving the following for {date} {t}:\n{meal.strip()}")
        else:
            try:
                meal = menu[date][mess][time]
            except KeyError:
                dispatcher.utter_message(text=f"{mess} does not serve anything for {date} {time}.")
            else:
                dispatcher.utter_message(text=f"{mess} is serving the following for {date} {time}:\n{meal.strip()}")

        print(mess)
        return [SlotSet("time", None), SlotSet("meal_time", None), SlotSet("mess", None)]

# TODO: Spell Checker, Form Cancel, Form Shift, Handle Form inform unhappy paths
