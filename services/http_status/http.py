from fastapi.exceptions import HTTPException

from http import HTTPStatus

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

