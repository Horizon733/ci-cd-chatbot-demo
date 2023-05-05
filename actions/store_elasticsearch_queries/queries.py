from typing import Text

from elasticsearch import Elasticsearch
es = Elasticsearch("http://elastic:root@localhost:9200")


class ElasticSearchQuery:

    def product_search_with_product_name(self, product_name: Text):
        product_search = {
                "_source": [],
                "size": 5,
                "query": {
                    "bool": {
                        "filter": [
                            {
                                "multi_match": {
                                    "query": product_name,
                                    "fields": [
                                        "description",
                                        "gender",
                                        "PrimaryColor",
                                        "ProductBrand",
                                        ":ProductName",
                                    ]
                                }
                            }
                        ]
                    }
                },
            }
        products = es.search(index="products", body=product_search, scroll="1m")
        return products

    def product_search_with_brand(self, brand: Text):
        product_search = {
            "_source": [],
            "size": 5,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "multi_match": {
                                "query": f"{brand}",
                                "fields": ["brand"],
                                "operator": "or",
                            }
                        }
                    ]
                }
            },
        }
        products = es.search(index="products", body=product_search, scroll="1m")
        return products

    def product_search_with_price(
            self, product_name: Text, price_min: int, price_max: int
    ):
        product_search = {
            "_source": [],
            "size": 5,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "multi_match": {
                                "query": product_name,
                                "type": "best_fields",
                                "fields": ["ProductName", "ProductBrand"],
                                "operator": "or",
                            }
                        },
                        {"range": {"Price (INR)": {"gte": price_min, "lte": price_max}}},
                    ]
                }
            },
        }
        products = es.search(index="products", body=product_search, scroll="1m")
        return products

    def product_search_with_brand_and_price(
        self, message: Text, price_min: int, price_max: int
    ):
        product_search = {
            "_source": [],
            "size": 5,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "multi_match": {
                                "query": message,
                                "type": "best_fields",
                                "fields": ["ProductBrand"],
                                "operator": "or",
                            }
                        },
                        {"range": {"Price (INR)": {"gte": price_min, "lte": price_max}}},
                    ]
                }
            },
        }
        products = es.search(index="products", body=product_search, scroll="1m")
        return products

    def product_search(self, slot_name: Text, **kwargs):
        method = f"product_search_with_{slot_name}"
        if hasattr(self, method) and callable(getattr(self, method)):
            product_search_funtion = getattr(self, method)
            return product_search_funtion(**kwargs)