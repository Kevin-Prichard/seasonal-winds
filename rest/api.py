#!/usr/bin/env python3

import logging
import mimetypes
import os

from quart import Quart, request, jsonify, Response
from quart.logging import default_handler


app = Quart(__name__)

logger = logging.getLogger(app.name)


@app.before_serving
def startup():
    pass


@app.route('/api/health', methods=['GET'])
async def health_check():
    return jsonify({"status": "OK"})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if not path:
        path = 'index3.html'

    candidate_path = f"public/{path}"
    if os.path.exists(candidate_path):
        try:
            with open(candidate_path, "rb") as f:
                response = Response(
                    f.read(), mimetype=mimetypes.guess_type(path)[0])
                return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
