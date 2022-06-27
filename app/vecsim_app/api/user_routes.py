import typing as t

from fastapi import APIRouter, Depends, Request, Response, encoders

from vecsim_app import schema
from vecsim_app import crud
from vecsim_app.auth import (
    get_current_active_superuser,
    get_current_active_user
)

users_router = r = APIRouter()


@r.get(
    "/users",
    response_model=t.List[schema.UserSchema],
    response_model_exclude_none=True,
)
async def users_list(
    response: Response,
    current_user=Depends(get_current_active_superuser),
):
    users = await crud.get_users()
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


@r.get(
    "/users/me",
    response_model=schema.UserSchema,
    response_model_exclude_none=True
)
async def user_me(current_user=Depends(get_current_active_user)):
    return current_user


@r.get(
    "/users/{user_id}",
    response_model=schema.UserSchema,
    response_model_exclude_none=True,
)
async def user_details(
    request: Request,
    user_id: int,
    current_user=Depends(get_current_active_superuser),
):
    user = await crud.get_user(user_id)
    return user


@r.post("/users",
        response_model=schema.UserSchema,
        response_model_exclude_none=True)
async def user_create(
    request: Request,
    user: schema.UserCreate,
    current_user=Depends(get_current_active_superuser),
):
    return await crud.create_user(user)


@r.put(
    "/users/{user_id}",
    response_model=schema.UserSchema,
    response_model_exclude_none=True,
)
async def user_edit(
    request: Request,
    user_id: int,
    user: schema.UserEdit,
    current_user=Depends(get_current_active_superuser),
):
    return await crud.update_user(user_id, user)


@r.delete(
    "/users/{user_id}",
    response_model=schema.UserSchema,
    response_model_exclude_none=True,
)
async def user_delete(
    request: Request,
    user_id: int,
    current_user=Depends(get_current_active_superuser),
):
    return await crud.delete_user(user_id)
