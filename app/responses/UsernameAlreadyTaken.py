from fastapi import status

from app.responses.BaseResponse import BaseResponse


class UsernameAlreadyTaken(BaseResponse):
    detail_message = "usernameAlreadyTaken"
    internal_code = "Y00"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, username: str):
        super().__init__(
            status_code=self.status_code,
            internal_status="KO",
            internal_code=self.internal_code,
            detail_message=self.detail_message,
            username=username,
        )
