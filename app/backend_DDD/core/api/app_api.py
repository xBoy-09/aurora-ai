import os
import json
import logging
import firebase_admin
import concurrent.futures
from firebase_admin import auth
import app.backend_DDD.core.api.utils as utils
import app.backend_DDD.core.api.schemas as schemas
from flask import Blueprint, Flask, request, jsonify
from app.backend_DDD.core.gpt.gpt_assistant_functions import GptAssistant
from app.backend_DDD.core.database.database_api_queries import DatabaseManager
from app.backend_DDD.core.commands import auth_commands as auth_cmds
from app.backend_DDD.core.commands import admin_commands as admin_cmds
from app.backend_DDD.core.classes import authentication as auth_class



# Initialize the Flask application
app = Flask(__name__)

# Create the Blueprint
ai_app = Blueprint("ai_app", __name__, url_prefix="/api/v1")
ai_app_admin = Blueprint("ai_app_admin", __name__, url_prefix="/api/v1/admin")
gpt_assistant = GptAssistant()
database = DatabaseManager()
# cred = firebase_admin.credentials.Certificate("app/backend_DDD/core/api/credentials-dev.json")
cred_json = os.environ.get('FIREBASE_CREDENTIALS')
cred = firebase_admin.credentials.Certificate(json.loads(cred_json))
# print(type(cred))
firebase_admin.initialize_app(cred)
# check if firebase_admin is initialized



@app.route("/", methods=["GET"])
def initFunction():
    users = auth.list_users(
        max_results=10,
    )
    print(f'Users: {users}')
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
        "email": schemas.QuerySchema,
        "user_id": schemas.QuerySchema,
        "full_name": schemas.QuerySchema,
    }
)
@ai_app.route("/create-user-without-firebase", methods=["POST"])
def create_user_without_firebase():
    try:
        req = request.get_json(force=True)
        email = req["email"]
        user_id = req["user_id"]
        full_name = req["full_name"]
        
        # Create the user
        uid = auth_cmds.create_user_without_firebase(
            email=email,
            user_id=user_id,
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
        print(f'Error in create_user_without_firebase: {e}')
        return utils.Response(
            message=f"An error occurred in server : {e}",
            status_code=500,
        ).__dict__
    

@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "uid": schemas.QuerySchema,
    }
)
@ai_app.route("/get-user", methods=["POST"])
def get_user():
    try:
        req = request.get_json(force=True)
        uid = req["uid"]
        
        #  Get user details
        user = auth_cmds.get_user(
            uid=uid,
            db_man=database,   
        )

        return utils.Response(
            message= f"User fetched successfully",
            status_code=200,
            data= user,
        ).__dict__


    except Exception as e:
        print(f'Error in create_user: {e}')
        return utils.Response(
            message=f"An error occurred in server : {e}",
            status_code=500,
        ).__dict__

@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={}
)
@ai_app.route("/get-university-setup-data", methods=["GET"])
def get_university_setup_data():
    try:
        
        #  Get user details
        user_setup = database.get_university_setup()

        return utils.Response(
            message= f"User setup fetched successfully",
            status_code=200,
            data= user_setup,
        ).__dict__


    except Exception as e:
        print(f'Error in get_university_setup_data: {e}')
        return utils.Response(
            message=f"An error occurred in server : {e}",
            status_code=500,
        ).__dict__
    

# TODO : Ensure user exist
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id" : schemas.QuerySchema,
    }
)

@ai_app.route("/skip-set-university-setup-data", methods=["POST"])
def skip_set_university_setup_data():
    try:
        req = request.get_json(force=True)
        user_id = req["user_id"]
        
        #  Get user details
        database.skip_set_university_setup(
            user_id=user_id,
        )

        return utils.Response(
            message= f"User setup skipped successfully",
            status_code=200,
        ).__dict__


    except Exception as e:
        print(f'Error in get_university_setup_data: {e}')
        return utils.Response(
            message=f"An error occurred in server : {e}",
            status_code=500,
        ).__dict__
    

# TODO : Ensure user exist
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id" : schemas.QuerySchema,
        "email" : schemas.QuerySchema,
        "affiliation" : schemas.QuerySchema,
        "school_id" : int,
        "major" : schemas.QuerySchema,
        "graduation_year" : int,
    }
)
@ai_app.route("/set-university-setup-data", methods=["POST"])
def set_university_setup_data():
    try:
        req = request.get_json(force=True)
        user_id = req["user_id"]
        email = req["email"]
        affiliation = req["affiliation"]
        school_id = req["school_id"]
        major = req["major"]
        graduation_year = req["graduation_year"]
        
        #  Get user details
        database.set_university_setup(
            user_id=user_id,
            email=email,
            affiliation=affiliation,
            school_id=school_id,
            major=major,
            graduation_year=graduation_year,
        )

        return utils.Response(
            message= f"User setup successfully",
            status_code=200,
        ).__dict__


    except Exception as e:
        print(f'Error in get_university_setup_data: {e}')
        return utils.Response(
            message=f"An error occurred in server : {e}",
            status_code=500,
        ).__dict__


@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "query": schemas.QuerySchema,
        "thread_id": schemas.QuerySchema,
        "user_id": schemas.QuerySchema,
    }
)
@ai_app.route("/gpt-public-query", methods=["POST"])
def gpt_public_query():
    try:
        query = request.get_json(force=True)["query"]
        thread_id = str(request.get_json(force=True)["thread_id"])
        user_id = request.get_json(force=True)["user_id"]

        if(len(thread_id) == 0):
            print('No thread id so getting new one')
            # set thread_id
            thread_id = gpt_assistant.get_thread_id(
                user_id=user_id,
            )

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    database.insert_user_threads,
                    thread_id=thread_id,
                    thread_name='',
                    user_id=user_id
                )


        print('Thread ID:', thread_id)
        # Process the query
        response = gpt_assistant.run_type_one(query=query, thread_id=thread_id)

        with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    database.updated_thread_time,
                    thread_id=thread_id,
                )

        return utils.Response(
            message="Query processed successfully",
            status_code=200,
            data= {
                "response": response.model_dump(),
                "thread_id": thread_id,
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
        "query": schemas.QuerySchema,
        "thread_id": schemas.QuerySchema,
        "user_id": schemas.QuerySchema,
    }
)
@ai_app.route("/get-thread-name", methods=["POST"])
def get_thread_name():
    try:
        query = request.get_json(force=True)["query"]
        thread_id = request.get_json(force=True)["thread_id"]
        user_id = request.get_json(force=True)["user_id"]

        if(len(thread_id) == 0):
            raise Exception("Thread id is required")

        # Process the query
        thread_name = gpt_assistant.run_get_thread_name(query=query, db_man=database)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                database.insert_user_threads,
                thread_id=thread_id,
                thread_name=thread_name,
                user_id=user_id
            )

        return utils.Response(
            message="Query processed successfully",
            status_code=200,
            data= {
                "thread_name": thread_name,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_thread_name: {e}')
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
    


@ai_app.route("/get-pdc-eateries", methods=["GET"])
def get_pdc_eateries():
    try:


        eateries = database.get_pdc_eateries()

        return utils.Response(
            message="Gotten thread messages successfully",
            status_code=200,
            data= {
                "messages": eateries,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_thread_messages: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    

@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "university_name": schemas.QuerySchema,
        "email_regex": schemas.QuerySchema,
        "assistant_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/add-data-university", methods=["POST"])
def get_thread_messages():
    try:
        user_id = request.get_json(force=True)["user_id"]
        university_name = request.get_json(force=True)["university_name"]
        email_regex = request.get_json(force=True)["email_regex"]
        assistant_id = request.get_json(force=True)["assistant_id"]

        # Add data to the university table
        database.admin.add_university(
            university_name=university_name,
            email_regex=email_regex,
            assistant_id=assistant_id,
        )

        return utils.Response(
            message="Data added successfully",
            status_code=200,
        ).__dict__
    except Exception as e:
        print(f'Error in get_thread_messages: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__



@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/get-universities", methods=["POST"])
def get_universities():
    try:
        universities = database.admin.view_all_universities()

        return utils.Response(
            message="Gotten universities successfully",
            status_code=200,
            data= {
                "universities": universities,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_universities: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__


@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/delete-university", methods=["POST"])
def delete_university():
    try:
        university_id = request.get_json(force=True)["university_id"]

        # Delete university
        database.admin.delete_university(university_id=university_id)

        return utils.Response(
            message="University deleted successfully",
            status_code=200,
        ).__dict__
    except Exception as e:
        print(f'Error in delete_university: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__

@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "university_name": schemas.QuerySchema,
        "email_regex": schemas.QuerySchema,
        "assistant_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/edit-university", methods=["POST"])
def edit_university():
    try:
        university_id = request.get_json(force=True)["university_id"]
        university_name = request.get_json(force=True)["university_name"]
        email_regex = request.get_json(force=True)["email_regex"]
        assistant_id = request.get_json(force=True)["assistant_id"]

        # Edit university
        database.admin.edit_university(
            university_id=university_id,
            university_name=university_name,
            email_regex=email_regex,
            assistant_id=assistant_id,
        )

        return utils.Response(
            message="University edited successfully",
            status_code=200,
        ).__dict__
    except Exception as e:
        print(f'Error in edit_university: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__

@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "university_id": schemas.QuerySchema,
        "majors_list": list[str],
        "school_name": schemas.QuerySchema,
        "school_name_abv": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/add-school-data", methods=["POST"])
def add_school_data():
    try:
        university_id = request.get_json(force=True)["university_id"]
        majors_list = request.get_json(force=True)["majors_list"]
        school_name = request.get_json(force=True)["school_name"]
        school_name_abv = request.get_json(force=True)["school_name_abv"]

        # Add school data
        database.admin.add_school_data(
            university_id=university_id,
            majors_list=majors_list,
            school_name=school_name,
            school_name_abv=school_name_abv,
        )

        return utils.Response(
            message="School data added successfully",
            status_code=200,
        ).__dict__
    except Exception as e:
        print(f'Error in add_school_data: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__

# add asistant
@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "assistant_id": schemas.QuerySchema,
        "assistant_name": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/add-assistant", methods=["POST"])
def add_assistant():
    try:
        user_id = request.get_json(force=True)["user_id"]
        assistant_id = request.get_json(force=True)["assistant_id"]
        assistant_name = request.get_json(force=True)["assistant_name"]

        # Add assistant
        database.admin.add_assistant(
            assistant_id=assistant_id,
            assistant_name=assistant_name,
        )
        
        return utils.Response(
            message="Assistant added successfully",
            status_code=200,
        ).__dict__
    except Exception as e:
        print(f'Error in add_assistant: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    
@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/get-assistants", methods=["POST"])
def get_assistants():
    try:
        assistants = admin_cmds.get_assistants(
            db=database,
            gpt=gpt_assistant,
        )

        return utils.Response(
            message="Gotten assistants successfully",
            status_code=200,
            data= {
                "assistants": assistants,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_assistants: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    

@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/get-users", methods=["POST"])
def get_users():
    try:
        users = admin_cmds.get_users(
            db=database,
        )

        return utils.Response(
            message="Gotten users successfully",
            status_code=200,
            data= {
                "users": users,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_users: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__
    

@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "user_id_for_details": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/get-user-details", methods=["POST"])
def get_user_details():
    try:
        user_id = request.get_json(force=True)["user_id_for_details"]

        # TODO: Implementation left
        user = admin_cmds.get_user_details(
            db=database,
            user_id=user_id,
        )

        return utils.Response(
            message="Gotten user details successfully",
            status_code=200,
            data= {
                "user": user,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_user_details: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__    



# Register the Blueprint with the Flask app
app.register_blueprint(ai_app)
app.register_blueprint(ai_app_admin)

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))  # Fallback to 5000 if PORT isn't set
    # app.run(host='0.0.0.0', port=port, debug=False)
    app.run()