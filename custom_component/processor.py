import locale
import logging
import re

import spacy
from typing import List, Text, Union
from spacy.tokens import Doc

from custom_component.duckling_parser import duckling_parse

logger = logging.getLogger(__name__)
NOUNS = ["NOUN", "PROPN"]
spacy_model = spacy.load("en_core_web_trf")


def extract_products(doc: Union[Doc, Doc]):
    extracted_entity = []
    product = ""
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            product += f"{token.text} "
    product = product.strip()
    extracted_entity.append({
        "type": "product",
        "text": product,
        "value": product
    })
    return extracted_entity


def extract_brands(doc: Union[Doc, Doc]):
    extracted_entity = []
    for single_entity in doc.ents:
        if single_entity.label_ == "ORG":
            brand_name = single_entity.text
            extracted_entity.append({
                "type": "brand",
                "text": brand_name,
                "value": brand_name
            })
    return extracted_entity


def extract_amount_of_money(doc: Union[Doc, Doc]):
    extracted_entity = []
    for single_entity in doc.ents:
        if single_entity.label_ == "MONEY":
            money_value = clean_amount(single_entity.text)
            extracted_entity.append({
                "type": "amount-of-money",
                "text": money_value,
                "value": money_value
            })
    return extracted_entity


def extract_email(pharse: Text):
    extracted_entity = []
    extracted_email = duckling_parse(pharse, dimensions=["email"])
    if len(extracted_email) > 0:
        extracted_entity.append({
            "type": "email",
            "text": extracted_email[0]["body"],
            "value": extracted_email[0]["body"]
        })
    return extracted_entity

def extract_number(pharse: Text):
    extracted_entity = []
    extracted_email = duckling_parse(pharse, dimensions=["number"])
    if len(extracted_email) > 0:
        extracted_entity.append({
            "type": "number",
            "text": extracted_email[0]["body"],
            "value": extracted_email[0]["body"]
        })
    return extracted_entity


def entity_parser(pharse) -> List:
    entities = []
    doc = spacy_model(pharse)
    entities += extract_email(pharse)
    entities += extract_number(pharse)
    entities += extract_amount_of_money(doc)
    entities += extract_brands(doc)
    entities += extract_products(doc)
    return entities


def clean_amount(value: Text):
    decimal_point_char = locale.localeconv()['decimal_point']
    return re.sub(r'[^0-9' + decimal_point_char + r']+', '', str(value))