
from flask import Flask, request, jsonify
from zeep import Client, helpers
from zeep.exceptions import Fault
from requests.exceptions import RequestException

app = Flask(__name__)

# Public SOAP service selected from the course document.
WSDL_URL = "https://footballpool.dataaccess.eu/info.wso?WSDL"


def get_stadiums():
    """Retrieve stadium names and convert the SOAP response."""
    client = Client(wsdl=WSDL_URL)
    response = client.service.StadiumNames()
    stadiums = helpers.serialize_object(response)

    if not isinstance(stadiums, list):
        raise ValueError("The SOAP service returned an invalid list.")

    return stadiums


def search_stadium(name):
    """Validate the input and search the SOAP stadium list."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Stadium name must be a non-empty string.")

    name = name.strip()

    if len(name) > 100:
        raise ValueError("Stadium name cannot exceed 100 characters.")

    stadiums = get_stadiums()

    # Validate each returned stadium name.
    if not all(isinstance(s, str) for s in stadiums):
        raise ValueError("The SOAP response contains invalid stadium names.")

    matches = [
        stadium for stadium in stadiums
        if name.lower() in stadium.lower()
    ]

    return {
        "search": name,
        "matches": matches,
        "count": len(matches)
    }


def process_request(name):
    """Return results or a custom error message."""
    try:
        return jsonify(search_stadium(name)), 200

    except ValueError as exc:
        return jsonify({
            "error": f"Stadium validation failed: {exc}"
        }), 400

    except (Fault, RequestException, Exception) as exc:
        return jsonify({
            "error": f"SOAP service request failed: {exc}"
        }), 502


@app.route("/stadiums", methods=["GET"])
def get_stadium():
    name = request.args.get("name")
    return process_request(name)


@app.route("/stadiums", methods=["POST"])
def post_stadium():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    return process_request(data.get("name"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
