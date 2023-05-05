from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.constants import *
from actions.utils import *


class ActionSearchProduct(Action):

    def name(self) -> Text:
        return "action_search_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = tracker.get_slot(PRODUCT)
        brand = tracker.get_slot(BRAND)
        price_min = tracker.get_slot(PRICE_MIN)
        price_max = tracker.get_slot(PRICE_MAX)
        slot_values = [product_name, brand, price_min, price_max]
        print(slot_values)
        return_values = []
        if any(i is None for i in slot_values):
            return_values.append(FollowupAction(PRODUCT_SEARCH_FORM))
        else:
            return_values.append(FollowupAction(ACTION_SHOW_PRODUCT))
        return return_values


class ActionShowProduct(Action):

    def name(self) -> Text:
        return "action_show_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = tracker.get_slot(PRODUCT)
        brand = tracker.get_slot(BRAND)
        price_min = tracker.get_slot(PRICE_MIN)
        price_max = tracker.get_slot(PRICE_MAX)
        filter_category = tracker.get_slot(FILTER_CATEGORY)
        dispatcher.utter_message("showing products")
        return []


class ActionAskOtp(Action):

    def name(self) -> Text:
        return "action_ask_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        otp = generate_otp()

        dispatcher.utter_message(response="utter_otp")

        return [SlotSet(OTP, otp)]
