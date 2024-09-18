import logging
from flask import Blueprint, Flask, request, jsonify
from core.api import utils
from core.api import schemas
from core.gpt.gpt_assistant_functions import GptAssistant

# Initialize the Flask application
app = Flask(__name__)

# Create the Blueprint
ai_app = Blueprint("ai_app", __name__, url_prefix="/api/v1")
gpt_assistant = GptAssistant()

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

# Run the server locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
