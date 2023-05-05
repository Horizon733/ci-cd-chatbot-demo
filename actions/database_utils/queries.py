import logging
import os
from typing import Text, List

from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_URL"])
logger = logging.getLogger(__name__)


def get_database():
    return client["ecomm"]


def get_table(table_name: Text):
    mydb = get_database()
    return mydb[table_name]


def insert_user_data(id: Text, email: Text, table_name: Text):
    try:
        user_table = get_table(table_name)
        user_data = {
            "_id": id,
            "email": email
        }
        response = user_table.insert_one(user_data)
        return response.acknowledged
    except Exception as e:
        logger.error(e)
        return False


def insert_order_data(email: Text, items: List, address: Text, table_name: Text):
    try:
        order_table = get_table(table_name)
        order_data = {
            "email": email,
            "address": address,
            "items": items
        }
        response = order_table.insert_one(order_data)
        return response.acknowledged
    except Exception as e:
        logger.error(e)
        return False


def insert_cart_data(email: Text, item: Text, table_name: Text):
    try:
        cart_table = get_table(table_name)
        cart_data = {
            "email": email,
            "item": item
        }
        response = cart_table.insert_one(cart_data)
        return response.acknowledged
    except Exception as e:
        logger.error(e)
        return False
