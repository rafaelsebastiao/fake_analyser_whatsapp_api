from requests import get, post, exceptions

from http import HTTPStatus

from fastapi import APIRouter

from fastapi.exceptions import HTTPException

from settings.settings import Settings



evolution_api_url = Settings().EVOLUTION_API_URL
apikey = Settings().AUTHENTICATION_API_KEY

router = APIRouter(
    prefix='/instances',
    tags = ['Instances']
)

@router.get('/messagesNotRead/')
async def messages_not_read():
    ...
