import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from vecsim_app import security
from vecsim_app.models import User
from vecsim_app.schema import UserCreate
from vecsim_app.schema.user import TokenData
from vecsim_app import crud
from vecsim_app.config import SECRET_KEY

async def get_current_user(token: str = Depends(security.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception
    user = await crud.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


async def authenticate_user(email: str, password: str):
    user = await crud.get_user_by_email(email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user


async def sign_up_new_user(
    email: str,
    password: str,
    title: str,
    company: str,
    first: str,
    last: str,
    ):
    try:
        user = await crud.get_user_by_email(email)
    # should raise exception that user is not found
    except HTTPException:
        new_user = UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            last_name=last,
            first_name=first,
            title=title,
            company=company
        )
        created_user = await crud.create_user(new_user)
        return created_user
    raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")