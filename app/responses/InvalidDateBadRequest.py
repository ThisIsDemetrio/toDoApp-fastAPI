from fastapi import status

from app.responses.BaseResponse import BaseResponse


class InvalidDateBadRequest(BaseResponse):
    detail_message = "Date is not valid"
    internal_code = "D01"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, key: str, value: str):
        super().__init__(
            status_code=self.status_code,
            internal_status="KO",
            internal_code=self.internal_code,
            detail_message=self.detail_message,
            key=key,
            value=value,
        )
