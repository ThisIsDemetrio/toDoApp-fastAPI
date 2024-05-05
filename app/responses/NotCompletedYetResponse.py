from fastapi import status

from app.responses.BaseResponse import BaseResponse


class NotCompletedYetResponse(BaseResponse):
    detail_message = "todoNotCompletedYet"
    internal_code = "C02"
    status_code = status.HTTP_200_OK

    def __init__(self, id: str):
        super().__init__(
            status_code=self.status_code,
            internal_status="KO",
            internal_code=self.internal_code,
            detail_message=self.detail_message,
            id=id,
        )
