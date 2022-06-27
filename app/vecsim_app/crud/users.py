import typing as t
from fastapi import HTTPException, status
from aredis_om.model.model import NotFoundError
from vecsim_app.security import get_password_hash
from vecsim_app import schema
from vecsim_app.models import User
from vecsim_app.db import get_current_user_count


async def get_user(user_id: int):
    user = await User.find(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def update_user(user_id: int, user: schema.UserEdit):
    # TODO allow user to update password
    user = await get_user(user_id)
    await user.update(**user.dict(exclude={"hashed_password", "password"}))

async def get_users() -> t.List[User]:
    users = await User.all_pks()
    all_users = [await User.get(pk) async for pk in users]
    if len(all_users) < 1:
        raise HTTPException(status_code=404, detail="Users not found")
    return all_users

async def get_user_by_email(email: str) -> schema.UserBase:
    try:
        user = await User.find(User.email == email).first()
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def create_user(user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    _id = await get_current_user_count()
    db_user = User(
        id=_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        title=user.title,
        company=user.company,
        hashed_password=hashed_password
    )
    await db_user.save()
    return db_user

async def delete_user(user_id: int):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    await user.delete()
    return user