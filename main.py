from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

from response import MessageRequest


async def send_message(client, phone, message):
    user_entity = await get_user_entity(client, phone)
    if user_entity:
        await client.send_message(entity=user_entity, message=message)
        message_id = await get_message_id(user_entity, client)
        response_data = MessageRequest(
            phone_number=phone, id=None, status=200, message_id=message_id
        )
    else:
        response_data = MessageRequest(
            phone_number=phone, id=None, status=404, message_id=None
        )
    return response_data


async def send_bulk_message(client, data):
    response_message_data_list = []
    await import_contacts(client, data['phone_numbers'])

    for phone in data['phone_numbers']:
        message_response = await send_message(client, phone, data['message'])
        response_message_data_list.append(message_response)

    await delete_contacts(client, response_message_data_list)

    return response_message_data_list


async def send_bulk_message_exclusive(client, data):
    response_message_data_list = []
    for user in data:
        message_response = await send_message(client, user["phone_number"], user["message"])
        response_message_data_list.append(message_response)
    return response_message_data_list


async def get_user_entity(client, phone):
    try:
        entity = await client.get_entity(phone)
        return entity
    except ConnectionError:
        print("Connection error.")
    except Exception:
        print("User does not exist.")


async def get_message_id(entity, client):
    messages = await client.get_messages(entity)
    return messages[0].id if messages else None


async def import_contacts(client, phone_numbers):
    contacts = [
        InputPhoneContact(client_id=0, phone=phone,
                          first_name='Customer ' + phone, last_name='')
        for phone in phone_numbers
    ]
    try:
        await client(ImportContactsRequest(contacts))
    except Exception as e:
        print(e)


async def delete_contacts(client, response_message_data_list):
    user_ids = [
        await get_user_id(client, response.phone_number) for response in response_message_data_list
    ]
    try:
        await client(DeleteContactsRequest(id=user_ids))
    except Exception:
        print("User is not deleted.")


async def get_user_id(client, phone):
    entity = await get_user_entity(client, phone)
    return entity.id if entity else None
