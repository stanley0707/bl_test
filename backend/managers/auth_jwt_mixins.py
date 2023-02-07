import os

from typing import Dict
from abc import ABC

from passlib.context import CryptContext
from jose import jwt
from fastapi.security import HTTPBearer
from fastapi import status, HTTPException, Depends

from .base_manager import BaseCRUD


class Token:
    credentials: str


class AuthJWTMixin(BaseCRUD, ABC):
    token_auth_scheme = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    ALGORITHM = os.environ.get("ALGORITHM")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = JWT_SECRET_KEY
    BROKEN_PERMISSIONS_MSG = "Sorry, you don't have a permission for this operation"
    INCORRECT_SESSION_MSG = (
        "Sorry, your session is not correct! Pleas, contact the administrator"
    )

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)

    async def create_refresh_token(self):
        """
        Must returns refresf token
        """
        return

    async def create_access_token(self, form_data) -> str:
        """
        Return token by loaded form_data from user
        :param form_data:
        :return:
        """
        if account := await self.get(email=form_data.username, raise_on=False):
            return jwt.encode(
                {"sub": str(account.email)}, self.JWT_SECRET_KEY, self.ALGORITHM
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    async def get_payload(self, token: Token) -> Dict:
        """
        Return decoded token as payload
        :param token:
        :return:
        """
        return jwt.decode(
            token.credentials, self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM]
        )

    async def is_admin(self, token: Token = Depends(token_auth_scheme)) -> None:
        """
        Return true if actual account is admin
        :param token:
        :return:
        """
        payload = await self.get_payload(token)
        if account := await self.get(email=payload["sub"]):
            if not account.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=self.BROKEN_PERMISSIONS_MSG,
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=self.INCORRECT_SESSION_MSG
            )

    async def is_authorize(self, token: Token = Depends(token_auth_scheme)) -> None:
        """
        Return true if actual account is user or admin
        :param token:
        :return:
        """
        payload = await self.get_payload(token)
        if account := await self.get(email=payload["sub"]):
            if not any([account.is_user, account.is_admin]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=self.BROKEN_PERMISSIONS_MSG,
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=self.INCORRECT_SESSION_MSG
            )

    async def get_current_session_account(
        self, token: Token = Depends(token_auth_scheme)
    ):
        """
        Returned acctual user by encoded session values
        :param token:
        :return:
        """
        payload = await self.get_payload(token)
        if account := await self.get(email=payload["sub"]):
            return account
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=self.INCORRECT_SESSION_MSG
        )
