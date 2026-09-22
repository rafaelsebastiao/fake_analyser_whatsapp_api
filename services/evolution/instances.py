from httpx import AsyncClient, _exceptions

from http import HTTPStatus

from fastapi.exceptions import HTTPException

from settings.settings import Settings

evolution_api_url = Settings().EVOLUTION_API_URL
apikey = Settings().EVOLUTION_AUTHENTICATION_API_KEY


def verify_status_http(response):
    if response.status_code != 200:
        if response.status_code == 401:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Unhautorized! Api Key is missing or is incorrect!'
            )
         
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Internal server error!"
            )


async def connect_instance(name : str, client: AsyncClient):
    try:
        response = await client.get(
            url=f"{evolution_api_url}/instance/connect/{name}",

            headers={
                "apikey":apikey
            },
            timeout=5
            )
    except _exceptions.ConnectError as errc:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                detail=f"Connection error: The Whatsapp's endpoint is inaccessible or down!\n"
                
            )

    verify_status_http(response)

    return response

async def find_instances(client: AsyncClient):
    try:
        response = await client.get(
            url=f'{evolution_api_url}/instance/fetchInstances',
            headers={
                "apikey":apikey
            },
            timeout=5

        )
    except _exceptions.ConnectError as errc:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
            detail=f"Connection error: The Whatsapp's endpoint is inaccessible or down!\n"
            
            )

    verify_status_http(response)
    return response


async def create_instance(name:str, client:AsyncClient):
    try:
        response = await client.post(
            url=f"{evolution_api_url}/instance/create",
            json={
                	"instanceName":name,
	                "integration":"WHATSAPP-BAILEYS"
            },

            headers={
                "apikey":apikey
            },
            timeout=5

            )
        
    except _exceptions.ConnectError as errc:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                detail=f"Connection error: The Whatsapp's endpoint is inaccessible or down!\n"
                
                )

    verify_status_http(response)
    return response