from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

from response import MessageRequest



async def send_message(client, phone, message):
        user_entity = await get_user_entity(phone, client)
        if user_entity is not None:
            await client.send_message(entity=user_entity, message=message)
            message_id = await get_message_id(user_entity, client)
            response_data = MessageRequest(
                phone_number=phone, id=None, status=200, message_id=message_id
            )

            return response_data
        else:
            response_data = MessageRequest(
                phone_number=phone, id=None, status=404, message_id=None
            )
            return response_data


async def send_bulk_message(client, phone_numbers, message):
    response_message_data_list = []
    await import_contacts(client,phone_numbers)

    for phone in phone_numbers:
        message_response = await send_message(client, phone, message)
        response_message_data_list.append(message_response)
    
    #return response_data
    user_id_list = []
    for phone in phone_numbers:
        entity = await get_user_entity(phone, client)
        user_id = await get_user_id(entity, client)   
        user_id_list.append(user_id)
        await delete_contact(client, user_id_list)
    
    return response_message_data_list

async def send_bulk_message_exclusive(client, data):
    response_message_data_list = []
    for user in data:
        message_response = await send_message(
            client, user["phone_number"], user["message"]
        )
        response_message_data_list.append(message_response)
    return response_message_data_list

async def get_user_entity(phone, client):
    try:
        entity = await client.get_entity(phone)
        return entity
    except ConnectionError:
        print("Connection error.")
    except:
        print("User does not exist.")

async def get_message_id(entity, client):
    message_id = await client.get_messages(entity)
    return message_id[0].id

async def get_user_id(entity, client):
    message_id = await client.get_messages(entity)
    return message_id[0].peer_id.user_id

async def import_contacts(client, phone_numbers):
    contacts = []
    try:
        for phone_number in phone_numbers: 
            contact = InputPhoneContact(client_id=0, phone=phone_number, first_name='Customer ' + phone_number, last_name='')          
            contacts.append(contact)    
        await client(ImportContactsRequest(contacts))
    except Exception as e:
        print(e)

async def delete_contact(client, user_id):
        try:
            await client(DeleteContactsRequest(id=user_id))
        except:
            print("user is not deleted.")