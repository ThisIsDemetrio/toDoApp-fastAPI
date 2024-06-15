from fastapi import status

from app.responses.BaseResponse import BaseResponse


class LimitNotValidBadRequest(BaseResponse):
    detail_message = "limitNotValid"
    internal_code = "D02"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            internal_status="KO",
            internal_code=self.internal_code,
            detail_message=self.detail_message,
        )
