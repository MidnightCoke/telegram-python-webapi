from flask import Flask, jsonify, request
from telethon import TelegramClient

from main import send_message, send_bulk_message_1_n, send_bulk_message_n_n
from response import ResponseData

app = Flask(__name__)


@app.route("/sendmessage", methods=["POST"])
async def send_message_api():
    request_data = request.get_json()
    response = await handle_send_message(request_data)
    return jsonify(response)


@app.route("/bulkmessage/1_n", methods=["POST"])
async def bulk_message_1_n_api():
    request_data = request.get_json()
    response = await handle_bulk_message(request_data, send_bulk_message_1_n)
    return jsonify(response)

@app.route("/bulkmessage/n_n", methods=["POST"])
async def bulk_message_n_n_api():
    request_data = request.get_json()
    response = await handle_bulk_message(request_data, send_bulk_message_n_n)
    return jsonify(response)

async def handle_send_message(request_data):
    session_id = request_data["config"]["session_id"]
    api_id = request_data["config"]["api_id"]
    api_hash = request_data["config"]["api_hash"]
    phone_number = request_data["data"]["phone_number"]
    message = request_data["data"]["message"]


    async with TelegramClient(session_id, api_id, api_hash) as client:
        result = await send_message(client, phone_number, message)

    response_data = ResponseData(Status=200, Description="", Result=result)
    return response_data


async def handle_bulk_message(request_data, send_func):
    session_id = request_data["config"]["session_id"]
    api_id = request_data["config"]["api_id"]
    api_hash = request_data["config"]["api_hash"]
    data = request_data["data"]
    
    
    async with TelegramClient(session_id, api_id, api_hash) as client:
        result = await send_func(client, data)

    response_data = ResponseData(Status=200, Description="", Result=result)
    return response_data


if __name__ == "__main__":
    app.run(debug=True)
