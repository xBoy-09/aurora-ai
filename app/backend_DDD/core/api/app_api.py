import os
import logging
import firebase_admin
import app.backend_DDD.core.api.utils as utils
import app.backend_DDD.core.api.schemas as schemas
from flask import Blueprint, Flask, request, jsonify
from app.backend_DDD.core.gpt.gpt_assistant_functions import GptAssistant
from app.backend_DDD.core.database.database_api_queries import DatabaseManager
from app.backend_DDD.core.commands import auth_commands as auth_cmds
from app.backend_DDD.core.classes import authentication as auth_class


# Initialize the Flask application
app = Flask(__name__)

# Create the Blueprint
ai_app = Blueprint("ai_app", __name__, url_prefix="/api/v1")
gpt_assistant = GptAssistant()
database = DatabaseManager()
cred = firebase_admin.credentials.Certificate("app/backend_DDD/core/api/credentials-dev.json")
firebase_admin.initialize_app(cred)


@app.route("/", methods=["GET"])
def initFunction():
    return "App is running"

# Define a route within the Blueprint
@ai_app.route("/test", methods=["GET"])
def test():
    return utils.Response(
        message="Test Response",
        status_code=200,
    ).__dict__

@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "email": schemas.QuerySchema,
        "password": schemas.QuerySchema,
        "full_name": schemas.QuerySchema,
    }
)
@ai_app.route("/create-user", methods=["POST"])
def create_user():
    try:
        req = request.get_json(force=True)
        email = req["email"]
        password = req["password"]
        full_name = req["full_name"]
        
        # Create the user
        uid = auth_cmds.create_user(
            email=email,
            password=password,
            full_name=full_name,
            fb_svc=auth_class.FirebaseService(),
            db_man=database,   
        )

        return utils.Response(
            message= f"User created successfully",
            status_code=200,
            data= {
                "uid": uid,
            },
        ).__dict__


    except Exception as e:
        print(f'Error in create_user: {e}')
        return utils.Response(
            message=f"An error occurred in server : {e}",
            status_code=500,
        ).__dict__


@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "query": schemas.QuerySchema,
    }
)
@ai_app.route("/gpt-public-query", methods=["POST"])
def gpt_public_query():
    try:
        query = request.get_json(force=True)["query"]

        # Process the query
        response = gpt_assistant.run_type_one(query=query)

        return utils.Response(
            message="Query processed successfully",
            status_code=200,
            data= {
                "response": response,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in gpt_public_query: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    

@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
    }
)
@ai_app.route("/get-user-threads", methods=["POST"])
def get_user_threads():
    try:
        user_id = request.get_json(force=True)["user_id"]

        threads = database.get_threads(user_id=user_id)

        return utils.Response(
            message="Gotten user threads successfully",
            status_code=200,
            data= {
                "threads": threads,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_user_threads: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    

@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "thread_id": schemas.QuerySchema,
    }
)
@ai_app.route("/add-user-thread", methods=["POST"])
def add_user_thread():
    try:
        user_id = request.get_json(force=True)["user_id"]
        thread_id = request.get_json(force=True)["thread_id"]

        database.add_thread(user_id=user_id, thread_id=thread_id)

        return utils.Response(
            message="Added user thread successfully",
            status_code=200,
        ).__dict__
    except Exception as e:
        print(f'Error in get_user_threads: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    

@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "thread_id": schemas.QuerySchema,
    }
)
@ai_app.route("/get-thread-messages", methods=["POST"])
def get_thread_messages():
    try:
        user_id = request.get_json(force=True)["user_id"]
        thread_id = request.get_json(force=True)["thread_id"]

        # TODO: Ensure thread exists against user

        messages = gpt_assistant.get_thread_messages(thread_id=thread_id)

        return utils.Response(
            message="Gotten thread messages successfully",
            status_code=200,
            data= {
                "messages": messages,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_thread_messages: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__



# Register the Blueprint with the Flask app
app.register_blueprint(ai_app)

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))  # Fallback to 5000 if PORT isn't set
    # app.run(host='0.0.0.0', port=port, debug=False)
    app.run()