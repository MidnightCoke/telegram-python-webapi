from flask import Flask, jsonify, request
from telethon import TelegramClient

from main import send_bulk_message, send_message, send_bulk_message_exclusive
from response import ResponseData

app = Flask(__name__)


@app.route("/sendmessage", methods=["POST"])
async def send_message_api():
    request_data = request.get_json()
    phone_number = request_data["data"]["phone_number"]
    message = request_data["data"]["message"]
    session_id = request_data["config"]["session_id"]
    api_id = request_data["config"]["api_id"]
    api_hash = request_data["config"]["api_hash"]

    
    client = TelegramClient(session_id, api_id, api_hash)

    async with client:
        result = await send_message(client, phone_number, message)

    response_data = ResponseData(Status=200, Description="", Result=result)
    return jsonify(response_data)


@app.route("/bulkmessage/ordinary", methods=["POST"])
async def ordinary_bulk_message_api():
    request_data = request.get_json()
    session_id = request_data["config"]["session_id"]
    api_id = request_data["config"]["api_id"]
    api_hash = request_data["config"]["api_hash"]
    phone_numbers = request_data["data"]["phone_numbers"]
    message = request_data["data"]["message"]

    
    client = TelegramClient(session_id, api_id, api_hash)

    async with client:
        result = await send_bulk_message(client, phone_numbers, message)
        
    
    response_data = ResponseData(Status=200, Description="", Result=result)
    return jsonify(response_data)


@app.route("/bulkmessage/exclusive", methods=["POST"])
async def exclusive_bulk_message_api():
    request_data = request.get_json()
    session_id = request_data["config"]["session_id"]
    api_id = request_data["config"]["api_id"]
    api_hash = request_data["config"]["api_hash"]
    data = request_data["data"]

    
    client = TelegramClient(session_id, api_id, api_hash)

    async with client:    
        result = await send_bulk_message_exclusive(client, data)
    
    response_data = ResponseData(Status=200, Description="", Result=result)
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
