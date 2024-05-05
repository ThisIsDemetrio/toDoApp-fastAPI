from fastapi import status

from app.responses.BaseResponse import BaseResponse


class SuccessResponse(BaseResponse):
    status_code = status.HTTP_200_OK

    def __init__(self, **kwargs):
        super().__init__(
            status_code=self.status_code, internal_status="OK", **kwargs
        )
