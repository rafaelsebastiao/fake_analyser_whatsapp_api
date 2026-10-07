import asyncio

from httpx import AsyncClient, _exceptions

from http import HTTPStatus

from fastapi.exceptions import HTTPException

from settings.settings import Settings

from services.http_status.http import verify_status_http

from pathlib import Path

evolution_api_url = Settings().EVOLUTION_API_URL
apikey = Settings().EVOLUTION_AUTHENTICATION_API_KEY

base_path = Path().cwd()

greetings_file_path = base_path / "templates" / "greetings.json"



async def get_phone_number(instanceName:str, client: AsyncClient, attempts:int = 6):
    try:
        response = await client.get(
            url=f'{evolution_api_url}/instance/fetchInstances',
            headers={'apikey': apikey},
            timeout=15
        
            )
    except _exceptions.ConnectError as errc:
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                    detail=f"Connection error: The Whatsapp's endpoint is inaccessible or down!\n"
                    
                )
    
    verify_status_http(response)


    phone_number = None

    for instance in response.json():
        if instance.get("name") == instanceName:
            phone_number =  instance.get("ownerJid")    
            break

    # repete o processo até o número de telefone for carregado ou esgotar as tentativas
    if not phone_number:
        if attempts <= 1:
            return ""
        await asyncio.sleep(2)
        
        return await get_phone_number(instanceName, client, attempts-1)

    return phone_number.split('@')[0]



async def send_text_message(
    instance_name: str,
    number:str,
    text:str, 
    client:AsyncClient
        ):
    
    try:
        response = await client.post(
            url = f'{evolution_api_url}/message/sendText/{instance_name}',
            json={
                "number":number,
                "text":text
            },

            headers={
                "apikey":apikey
            },

            timeout=15
        )
    except _exceptions.ConnectError as errc:
                    raise HTTPException(
                        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                        detail=f"Connection error: The Whatsapp's endpoint is inaccessible or down!\n"
                        
                    )
        
    verify_status_http(response)
    return response.json()

