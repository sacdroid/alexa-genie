from app.alexa import AlexaRequest
from app.handlers import dispatch
from flask import Flask, abort, jsonify, request
from app import app
from app import settings
@app.route('/alexa', methods=['POST'])
def incoming_alexa_request():
    print(request.data)
    try:
        alexa_request = AlexaRequest(request)
    except ValueError:
        abort(400)
    
    if alexa_request.is_valid():
        alexa_response = dispatch(alexa_request)
    else:
        abort(403)
    return jsonify(alexa_response.to_dict())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=(settings.CERTIFICATE_PATH, settings.PRIVATE_KEY_PATH)) 

