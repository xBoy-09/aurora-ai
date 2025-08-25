import logging
import app.backend_DDD.core.api.utils as utils
import app.backend_DDD.core.api.schemas as schemas
from flask import Blueprint, request
from app.backend_DDD.core.commands import admin_commands as admin_cmds
from app.backend_DDD.core.gpt.gpt_assistant_functions import GptAssistant
from app.backend_DDD.core.database.database_api_queries import DatabaseManager

# Add this after your imports
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the admin Blueprint
ai_app_admin = Blueprint("ai_app_admin", __name__, url_prefix="/api/v1/admin")

# Initialize dependencies
gpt_assistant = GptAssistant()
database = DatabaseManager()

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
def add_data_university():
    logging.info("Endpoint Hit: /api/v1/admin/add-data-university [POST]")
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
        print(f'Error in add_data_university: {e}')
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
    logging.info("Endpoint Hit: /api/v1/admin/get-universities [POST]")
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
        "university_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/delete-university", methods=["POST"])
def delete_university():
    logging.info("Endpoint Hit: /api/v1/admin/delete-university [POST]")
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
        "university_id": schemas.QuerySchema,
        "university_name": schemas.QuerySchema,
        "email_regex": schemas.QuerySchema,
        "assistant_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/edit-university", methods=["POST"])
def edit_university():
    logging.info("Endpoint Hit: /api/v1/admin/edit-university [POST]")
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
    logging.info("Endpoint Hit: /api/v1/admin/add-school-data [POST]")
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
    logging.info("Endpoint Hit: /api/v1/admin/add-assistant [POST]")
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
    logging.info("Endpoint Hit: /api/v1/admin/get-assistants [POST]")
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
    logging.info("Endpoint Hit: /api/v1/admin/get-users [POST]")
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
    logging.info("Endpoint Hit: /api/v1/admin/get-user-details [POST]")
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


# get all feedback
@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/get-all-feedback", methods=["POST"])
def get_all_feedback():
    logging.info("Endpoint Hit: /api/v1/admin/get-all-feedback [POST]")
    try:
        feedback = database.admin.get_all_feedback()
        return utils.Response(
            message="Gotten all feedback successfully",
            status_code=200,
            data= {
                "feedback": feedback,
            },
        ).__dict__
    except Exception as e:
        print(f'Error in get_all_feedback: {e}')
        return utils.Response(
            message=f"An error occurred in server",
            status_code=500,
        ).__dict__



@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "user_id": schemas.QuerySchema,
        "feedback_id": schemas.QuerySchema,
        "status": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/change-feedback-status", methods=["POST"])
def change_feedback_status():
    logging.info("Endpoint Hit: /api/v1/admin/change-feedback-status [POST]")
    try:
        payload = request.get_json(force=True)
        user_id = payload["user_id"]
        feedback_id = payload["feedback_id"]
        status = payload["status"]

        # Update feedback status in the database
        result = database.admin.change_feedback_status(feedback_id=feedback_id, status=status)

        if result:
            return utils.Response(
                message="Feedback status updated successfully",
                status_code=200,
                data={"feedback_id": feedback_id, "status": status},
            ).__dict__
        else:
            return utils.Response(
                message="Failed to update feedback status",
                status_code=400,
            ).__dict__
    except Exception as e:
        print(f'Error in change_feedback_status: {e}')
        return utils.Response(
            message="An error occurred in server",
            status_code=500,
        ).__dict__

@utils.require_admin(database=database)
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "feedback_id": schemas.QuerySchema,
        "comment": schemas.QuerySchema,
    }
)
@ai_app_admin.route("/add-feedback-comment", methods=["POST"])
def add_feedback_comment():
    logging.info("Endpoint Hit: /api/v1/admin/add-feedback-comment [POST]")
    try:
        payload = request.get_json(force=True)
        feedback_id = payload["feedback_id"]
        comment = payload["comment"]

        # Add comment to feedback in the database
        result = database.admin.add_comment_to_feedback(feedback_id=feedback_id, comment=comment)

        if result:
            return utils.Response(
                message="Comment added to feedback successfully",
                status_code=200,
                data={"feedback_id": feedback_id, "comment": comment},
            ).__dict__
        else:
            return utils.Response(
                message="Failed to add comment to feedback",
                status_code=400,
            ).__dict__
    except Exception as e:
        print(f'Error in add_feedback_comment: {e}')
        return utils.Response(
            message="An error occurred in server",
            status_code=500,
        ).__dict__
