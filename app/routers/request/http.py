from fastapi import APIRouter

from app.handler.fatcory import FantasyResponse
from app.middleware.AsyncHttpClient import AsyncHttpClient
from app.schema.http import HttpRequestForm

router = APIRouter(prefix="/request")


@router.post("/http")
async def request_http(data: HttpRequestForm):
    try:
        r = await AsyncHttpClient.client(data.url, data.body_type, headers=data.headers, body=data.body)
        response = await r.invoke(data.method)
        if response.get("status"):
            return FantasyResponse.success(response)
        return FantasyResponse.failed(response.get("msg"), data=response)
    except Exception as e:
        print(e)
        return FantasyResponse.failed(e)
