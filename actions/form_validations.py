from typing import Text, Dict, List

from rasa.shared.core.constants import REQUESTED_SLOT
from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.constants import *
from actions.utils import to_snake_case


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    def validate_email(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            return {EMAIL: value}
        else:
            return {REQUESTED_SLOT: EMAIL}

    def validate_otp(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        correct_otp = tracker.get_slot("CORRECT_OTP")
        if value == correct_otp:
            return {OTP: value}
        else:
            return {REQUESTED_SLOT: OTP}


class ValidateProductSearchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_product_search_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()
        filter_category = tracker.get_slot(FILTER_CATEGORY)
        if filter_category == FILTER_CATEGORY_PRODUCT:
            return slots + PRODUCT
        elif filter_category == FILTER_CATEGORY_BRAND:
            return slots + BRAND
        elif filter_category == FILTER_CATEGORY_PRICE:
            return slots + [PRODUCT, PRICE_MIN, PRICE_MAX]
        elif filter_category == FILTER_CATEGORY_BRAND_AND_PRICE:
            return slots + [BRAND, PRICE_MIN, PRICE_MAX]
        return slots

    def validate_filter_category(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        if to_snake_case(value) in FILTER_CATEGORIES:
            return {FILTER_CATEGORY: to_snake_case(value)}
        else:
            return {REQUESTED_SLOT: FILTER_CATEGORY}

    def extract_product(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        product = tracker.get_slot(PRODUCT)
        if product is not None:
            return {PRODUCT: product}
        else:
            return {REQUESTED_SLOT: PRODUCT}

    def extract_brand(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        brand = tracker.get_slot(BRAND)
        if brand is not None:
            return {BRAND: brand}
        else:
            return {REQUESTED_SLOT: BRAND}

    def extract_price_min(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        price_min = tracker.get_slot(PRICE_MIN)
        if price_min is not None:
            return {PRICE_MIN: price_min}
        else:
            return {REQUESTED_SLOT: PRICE_MIN}

    def extract_price_max(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Dict[str, str]:
        price_max = tracker.get_slot(PRICE_MAX)
        if price_max is not None:
            return {PRICE_MAX: price_max}
        else:
            return {REQUESTED_SLOT: PRICE_MAX}
