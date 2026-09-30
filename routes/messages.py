from requests import get, post, exceptions

from http import HTTPStatus

from fastapi import APIRouter

from fastapi.requests import Request

from fastapi.exceptions import HTTPException

from settings.settings import Settings



evolution_api_url = Settings().EVOLUTION_API_URL
apikey = Settings().EVOLUTION_AUTHENTICATION_API_KEY

router = APIRouter(
    prefix='/messages',
    tags = ['messages']
)

@router.post('/new-message/')
async def post_message(request: Request):
    payload = await request.json()
    print(payload)
    return {"ok": True}


@router.get('/messagesNotRead/')
async def messages_not_read():
    ...
