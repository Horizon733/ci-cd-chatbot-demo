import logging
from typing import Dict, Any, List, Text

from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.constants import ENTITIES, TEXT
from rasa.nlu.extractors.extractor import EntityExtractorMixin
from rasa.shared.nlu.training_data.message import Message

from custom_component.processor import entity_parser


logger = logging.getLogger(__name__)


def extract_value(match: Dict[Text, Any]) -> Dict[Text, Any]:
    if match["value"].get("type") == "interval":
        value = {
            "to": match["value"].get("to", {}).get("value"),
            "from": match["value"].get("from", {}).get("value"),
        }
    else:
        value = match["value"].get("value")

    return value


def convert_custom_format_to_rasa(
        matches: List[Dict[Text, Any]]
) -> List[Dict[Text, Any]]:
    extracted = []

    for match in matches:
        entity = {
            "text": match.get("body", match.get("text", None)),
            "value": match["value"],
            "confidence": 1.0,
            "additional_info": match["value"],
            "entity": match["type"],
        }

        extracted.append(entity)

    return extracted


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR, is_trainable=False
)
class CustomEntityExtractor(GraphComponent, EntityExtractorMixin):

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "dimension": None,
            "timeout": 3
        }

    def __init__(
            self,
            config: Dict[Text, Any]
    ) -> None:
        self.component_config = config

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> "CustomEntityExtractor":
        return cls(config)

    def _payload(self, text: Text) -> Dict[Text, Any]:
        language = self.component_config["language"]
        return {
            "text": text,
            "language": language,
        }

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            matches = entity_parser(message.get(TEXT))
            all_extracted = convert_custom_format_to_rasa(matches)
            extracted = self.filter_irrelevant_entities(all_extracted, self.component_config["dimensions"])
            extracted = self.add_extractor_name(extracted)
            message.set(
                ENTITIES, message.get(ENTITIES, []) + extracted, add_to_output=True
            )
            logger.debug(f"messages: {message}")
        return messages

