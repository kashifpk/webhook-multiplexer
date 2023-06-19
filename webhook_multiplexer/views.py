import uuid

import httpx
from fastapi import APIRouter, status, Depends, HTTPException, Request

from .data import forwards_data
from .depends import authenticated_request
from .schemas import CreateForwardRequest

router = APIRouter()


@router.get("/_", status_code=status.HTTP_200_OK, response_model=dict)
async def get_forwards(_=Depends(authenticated_request)):
    return forwards_data._data


@router.post("/_", status_code=status.HTTP_201_CREATED, response_model=dict)
async def add_forward(data: CreateForwardRequest, _=Depends(authenticated_request)):
    for incoming_key, values_dict in forwards_data._data.items():
        if incoming_key == data.incoming and data.outgoing in values_dict:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Already present")

    if data.incoming not in forwards_data._data:
        forwards_data.__class__._data[data.incoming] = {}

    key = str(uuid.uuid4())[:8]
    forwards_data.__class__._data[data.incoming][data.outgoing] = {"key": key}
    forwards_data.save_data()

    return forwards_data._data


@router.delete("/_/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_forward(key: str, _=Depends(authenticated_request)):
    print(key)
    for _, outgoing_map in forwards_data._data.items():
        for outgoing_url, outgoing_dict in outgoing_map.items():
            if outgoing_dict["key"] == key:
                del outgoing_map[outgoing_url]
                forwards_data.save_data()
                return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")


@router.get("/_refresh", status_code=status.HTTP_200_OK, response_model=dict)
async def refresh_forwards(_=Depends(authenticated_request)):
    forwards_data.load_data()
    return forwards_data._data


@router.post("/{endpoint:path}", status_code=status.HTTP_200_OK)
async def post_forwarder(endpoint: str, request: Request):
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    if endpoint in forwards_data._data:
        print("Matched routes")
        request_body = await request.body()

        for target_url in forwards_data._data[endpoint].keys():
            print(target_url)

            async with httpx.AsyncClient() as client:
                await client.post(
                    target_url,
                    headers=request.headers,
                    params=request.query_params,
                    cookies=request.cookies,
                    content=request_body
                )


    # print(endpoint)
    # print(request.method)
    # print(request.url)
    # print(request.headers)
    # print(request.query_params)
    # print(request.client.host)
    # print(request.cookies)

    # print(await request.body())
    return "Accpeted"
