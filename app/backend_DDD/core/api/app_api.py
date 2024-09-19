import logging
from flask import Blueprint, Flask, request, jsonify
from app.backend_DDD.core.gpt.gpt_assistant_functions import GptAssistant
import app.backend_DDD.core.api.utils as utils
import app.backend_DDD.core.api.schemas as schemas
import os


# Initialize the Flask application
app = Flask(__name__)

# Create the Blueprint
ai_app = Blueprint("ai_app", __name__, url_prefix="/api/v1")
gpt_assistant = GptAssistant()


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
        "query": schemas.QuerySchema,
    }
)
@ai_app.route("/gpt-public-query", methods=["POST"])
def gpt_public_query():
    query = request.get_json(force=True)["query"]

    # Process the query
    response, image, link = gpt_assistant.process_public_query(query)

    return utils.Response(
        message="Query processed successfully",
        status_code=200,
        data= {
            "response": response,
            "image": image,
            "link" : link,
        },
    ).__dict__

# Register the Blueprint with the Flask app
app.register_blueprint(ai_app)

if __name__ == '__main__':
    # Heroku assigns the port dynamically, and it's available in the environment variable PORT
    # port = int(os.environ.get('PORT', 5000))  # Fallback to 5000 if PORT isn't set
    # app.run(host='0.0.0.0', port=port, debug=False)
    app.run()