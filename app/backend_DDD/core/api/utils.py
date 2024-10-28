import logging
import os
from abc import ABCMeta
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps
from typing import Dict, List, Optional, Union
from uuid import NAMESPACE_OID, uuid5
from flask import request , jsonify
from app.backend_DDD.core.api.event_codes import EventCode
from app.backend_DDD.core.database.database_api_queries import DatabaseManager as db_man


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



def require_admin(database):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                user_id = request.get_json(force=True).get("user_id")
                if not user_id:
                    return jsonify({
                        "message": "User ID is missing.",
                        "status_code": 400
                    })

                # Check if the user is an admin
                user = database.get_user(user_id)
                if not user or user.get('user_type') != 'admin':
                    return jsonify({
                        "message": "Access denied. Admin privileges are required.",
                        "status_code": 403
                    })

                return f(*args, **kwargs)
            except Exception as e:
                print(f"Error in require_admin: {e}")
                return jsonify({
                    "message": "An error occurred in server.",
                    "status_code": 500
                })

        return decorated_function
    return decorator



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