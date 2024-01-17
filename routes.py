from flask import jsonify, request, Blueprint
from intent_handlers import handle_intent

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def webhook_route():
    try:
        req = request.get_json(force=True)
        response = handle_intent(req)
        return jsonify(response)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'fulfillmentText': 'An error occurred. Please try again later.'})
