import json

from pathlib import Path

from services.evolution.messages import get_phone_number, send_text_message

from settings.settings import Settings

base_path = Path().cwd()

greetings_file_path = base_path / "templates" / "greetings.json"



def get_default_message():
    with open(greetings_file_path, 'r', encoding='utf-8') as file:
        content = json.load(file)

    return content["text"]


async def handle_connection_update(payload: dict, client):
    data = payload.get("data", {})

    if data.get("state") != "open":
        return

    instance_name = payload.get("instance")

    phone_number = await get_phone_number(instanceName=instance_name, client=client)    


    if phone_number == "":
        ...
    
    await send_text_message(
        instance_name=instance_name, 
        number=phone_number, 
        text=get_default_message(), 
        client=client)







evolution_api_url = Settings().EVOLUTION_API_URL
evolution_api_key = Settings().EVOLUTION_AUTHENTICATION_API_KEY



async def handle_message_upsert(payload: dict, client):
    data = payload.get("data")

    
    print(data)
    

    remote_jid = data.get("key").get("remoteJid")

    print(remote_jid)

    await send_text_message(
        instance_name="fake-analyser",
        number=remote_jid,
        text=get_default_message(),
        client=client,
    )

