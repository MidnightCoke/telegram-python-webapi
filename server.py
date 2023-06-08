from flask import Flask, jsonify, request
from telethon import TelegramClient
from telethon.sessions import StringSession

from main import send_bulk_message_1_n, send_bulk_message_n_n
from response import ResponseData

app = Flask(__name__)


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


async def handle_bulk_message(request_data, send_func):
    session_id = request_data["config"]["session_id"]
    api_id = request_data["config"]["api_id"]
    api_hash = request_data["config"]["api_hash"]
    data = request_data["data"]

    async with TelegramClient(StringSession(session_id), api_id, api_hash) as client:
        result = await send_func(client, data)

    response_data = ResponseData(Status=200, Description="", Result=result)
    return response_data


if __name__ == "__main__":
    app.run(debug=True)
