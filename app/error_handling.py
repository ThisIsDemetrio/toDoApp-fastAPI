from app.ErrorCode import ErrorCode


error_description_map: dict = {
    ErrorCode.A01: "idNotFoundInDatabase",
    ErrorCode.C01: "todoAlreadyCompleted",
    ErrorCode.C02: "todoNotCompletedYet",
    ErrorCode.C03: "remainderNotFound",
    ErrorCode.U00: "unhandledException",
    ErrorCode.Y00: "usernameAlreadyTaken",
}


class BadRequestDetail:
    DATE_NOT_VALID = "date not valid"


class ErrorModel:
    status = ("KO",)
    code: str
    message: str


def return_error(error_code: ErrorCode, **kwargs):
    error_description = error_description_map.get(error_code, None)
    if error_description is None:
        raise KeyError(error_code)

    result: ErrorModel = {
        "status": "KO",
        "code": error_code,
        "message": error_description,
    }

    return {**result, **kwargs}
