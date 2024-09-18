import logging
import os
from abc import ABCMeta
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps
from typing import Dict, List, Optional, Union
from uuid import NAMESPACE_OID, uuid5
from flask import request
from event_codes import EventCode


@dataclass(frozen=True)
class Response:
    """Response object"""

    message: str
    status_code: int
    data: Union[Dict, List] = None


@dataclass
class CustomException(Exception):
    message: str = "An error occurred"
    status_code: int = 400
    event_code: EventCode = EventCode.DEFAULT_EVENT

def handle_missing_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.json is None:
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "PayloadMissingInRequest",
                },
            )
            raise CustomException(message="payload missing in request")
        return func(*args, **kwargs)

    return wrapper

def validate_and_sanitize_json_payload(
    required_parameters: Dict[str, ABCMeta],
    optional_parameters: Optional[Dict[str, ABCMeta]] = None,
):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req = request.get_json(force=True)

            if "RETOOL_SECRET" in req.keys():
                req.pop("RETOOL_SECRET")

            if "RP_SECRET" in req.keys():
                req.pop("RP_SECRET")

            if "EXTERNAL_OTP_SECRET" in req.keys():
                req.pop("EXTERNAL_OTP_SECRET")

            # Remove all optional parameters from the request
            if optional_parameters is not None:
                for k, _ in optional_parameters.items():
                    req.pop(k, None)

            if set(required_parameters) != set(req.keys()):
                logging.info(
                    {
                        "message": "Custom exception raised",
                        "endpoint": "api-decorator",
                        "exception_type": "InvalidJsonPayload",
                        "json_request": req,
                    },
                )
                raise CustomException("invalid json payload, missing or extra parameters")

            for param, schema in required_parameters.items():
                # Assuming that all input strings should not contain leading or trailing whitespaces
                if isinstance(req[param], str):
                    req[param] = req[param].strip()

                try:
                    schema(req[param]).validate()
                except CustomException as e:
                    logging.info(
                        {
                            "message": "Custom exception raised",
                            "endpoint": "api-decorator",
                            "exception_type": "InvalidSchema",
                        },
                    )
                    raise e

            return func(*args, **kwargs)

        return wrapper

    return inner_decorator