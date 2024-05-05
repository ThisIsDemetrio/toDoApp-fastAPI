from fastapi import status
from fastapi.responses import JSONResponse


class InvalidDateBadRequest(JSONResponse):
    detail_message = "Date is not valid"

    def __init__(self, key: str, value: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": self.detail_message,
                "key": key,
                "value": value,
            },
        )
