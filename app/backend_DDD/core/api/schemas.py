from dataclasses import dataclass
from abc import ABC, abstractmethod
import app.backend_DDD.core.api.utils as utils


@dataclass()
class AbstractSchema(ABC):
    @abstractmethod
    def validate(self):
        pass


@dataclass()
class QuerySchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Query passed is not a string")