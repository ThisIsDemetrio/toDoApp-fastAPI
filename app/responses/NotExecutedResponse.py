from fastapi import status

from app.responses.BaseResponse import BaseResponse


class NotExecutedResponse(BaseResponse):
    detail_message = "notExecuted"
    internal_code = "U00"
    status_code = status.HTTP_200_OK

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            internal_status="KO",
            internal_code=self.internal_code,
            detail_message=self.detail_message,
        )
