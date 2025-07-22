from flask import Flask, jsonify, request

from app.calculator import add, divide, multiply, subtract

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(
        {"status": "healthy", "service": "math_utils_api", "version": "0.1.0"}
    )


@app.route("/health", methods=["GET"])
def health():
    """Alternative health check endpoint."""
    return jsonify({"status": "ok"})


def validate_request_data(data):
    """Validate that request contains required numeric data."""
    if data is None:
        return False, "No JSON data provided"

    if "a" not in data or "b" not in data:
        return False, "Missing required parameters 'a' and 'b'"

    try:
        float(data["a"])
        float(data["b"])
    except (ValueError, TypeError):
        return False, "Parameters 'a' and 'b' must be numeric"

    return True, None


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/add", methods=["POST"])
def add_route():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        is_valid, error_msg = validate_request_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        result = add(data["a"], data["b"])
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/subtract", methods=["POST"])
def subtract_route():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        is_valid, error_msg = validate_request_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        result = subtract(data["a"], data["b"])
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/multiply", methods=["POST"])
def multiply_route():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        is_valid, error_msg = validate_request_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        result = multiply(data["a"], data["b"])
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/divide", methods=["POST"])
def divide_route():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400

        is_valid, error_msg = validate_request_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        result = divide(data["a"], data["b"])
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
