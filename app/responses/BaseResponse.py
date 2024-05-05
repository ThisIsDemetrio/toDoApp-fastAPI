from typing import Literal
from fastapi import status
from fastapi.responses import JSONResponse


class BaseResponse(JSONResponse):
    def __init__(
        self,
        status_code: status = status.HTTP_200_OK,
        internal_status: Literal["OK", "KO"] = "OK",
        internal_code: str = None,
        detail_message: str = None,
        **kwargs
    ):
        content = {
            "status": internal_status,
            **kwargs,
        }

        if internal_code is not None:
            content["code"] = internal_code

        if detail_message is not None:
            content["detail"] = detail_message

        super().__init__(
            status_code=status_code,
            content=content,
        )
