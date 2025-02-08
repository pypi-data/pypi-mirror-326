from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from quixstreams import Application
from pydantic import BaseModel
from typing import Any, Dict
from tenacity import retry, wait_exponential, stop_after_attempt


class ClassificationInferenceData(BaseModel):
    features: list
    prediction: Any
    probabilities: list
    model_version: str
    timestamp: int


class RegressionInferenceData(BaseModel):
    features: list
    prediction: Any
    model_version: str
    timestamp: int


class BaseClassificationInferenceHandler(AbstractContextManager, ABC):
    def __init__(self, kafka_config: Dict[str, Any]):
        self._app = Application(
            broker_address=kafka_config.get("bootstrap_servers", "localhost:9092"),
            consumer_group=kafka_config.get("consumer_group", "mloptiflow-monitoring"),
            auto_offset_reset="latest",
        )
        self._topic = self._app.topic(name=kafka_config["topic_name"])
        self._producer = None

    def __enter__(self):
        self._producer = self._app.get_producer()
        return self

    def __exit__(self, *args):
        if self._producer:
            self._producer.close()

    @abstractmethod
    def serialize(self, data: ClassificationInferenceData) -> Dict:
        pass

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3)
    )
    def stream(self, data: ClassificationInferenceData):
        serialized = self.serialize(data)
        self._producer.produce(
            topic=self._topic.name,
            key=data.model_version,
            value=serialized,
        )


class BaseRegressionInferenceHandler(AbstractContextManager, ABC):
    def __init__(self, kafka_config: Dict[str, Any]):
        self._app = Application(
            broker_address=kafka_config.get("bootstrap_servers", "localhost:9092"),
            consumer_group=kafka_config.get("consumer_group", "mloptiflow-monitoring"),
            auto_offset_reset="latest",
        )
        self._topic = self._app.topic(name=kafka_config["topic_name"])

    def __enter__(self):
        self._producer = self._app.get_producer()
        return self

    def __exit__(self, *args):
        if self._producer:
            self._producer.close()

    @abstractmethod
    def serialize(self, data: RegressionInferenceData) -> Dict:
        pass

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3)
    )
    def stream(self, data: RegressionInferenceData):
        serialized = self.serialize(data)
        self._producer.produce(
            topic=self._topic.name,
            key=data.model_version,
            value=serialized,
        )
