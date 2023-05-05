import json
import logging
import os
from typing import Text, Dict, Any, List

import requests

logger = logging.getLogger(__name__)


def get_payload(text: Text, locale: Text, dimensions: List[Text]) -> Dict[Text, Any]:
    return {
        "text": text,
        "locale": locale,
        "dims": json.dumps(dimensions),
    }


def duckling_parse(text: Text, dimensions: List[Text], timeout: int = 3, locale: Text = None) -> List[Dict[Text, Any]]:
    """Sends the request to the duckling server and parses the result.
    Args:
        text: Text for duckling server to parse.
        timeout: Timeout integer in seconds (default 3secs)
        locale: locale like en_US which defines language_countrycode (not provided then duckling will use default)
        dimensions: entity name list
    Returns:
        JSON response from duckling server with parse data.
    """
    parse_url = f"{os.environ.get('DUCKLING_URL', 'http://localhost:8000')}/parse"
    try:
        payload = get_payload(text, locale, dimensions)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        response = requests.post(
            parse_url,
            data=payload,
            headers=headers,
            timeout=timeout,
        )
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"Failed to get a proper response from remote "
                f"duckling at '{parse_url}. "
                f"Status Code: {response.status_code}. "
                f"Response: {response.text}"
            )
            return []
    except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
    ) as e:
        logger.error(
            "Failed to connect to duckling http server. Make sure "
            "the duckling server is running/healthy/not stale and the proper host "
            "and port are set in the configuration. More "
            "information on how to run the server can be found on "
            "github: "
            "https://github.com/facebook/duckling#quickstart "
            "Error: {}".format(e)
        )
        return []
