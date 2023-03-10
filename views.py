from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from builder import build_query
from models import BatchRequestSchema

main_bp = Blueprint('main', __name__)
FILE_NAME = 'data/apache_logs.txt'


@main_bp.route('/perform_query', methods=['POST'])
def perform_query():
    data = request.json
    try:
        validates_data = BatchRequestSchema().load(data)
    except ValidationError as error:
        print(error.messages)
        return jsonify(error.messages), 400
    result = None

    for query in validates_data['queries']:
        result = build_query(
            cmd=query['cmd'],
            value=query['value'],
            file_name=FILE_NAME,
            data=result,
        )

    return jsonify(result)


@main_bp.route('/ping')
def ping():
    return 'pong'
