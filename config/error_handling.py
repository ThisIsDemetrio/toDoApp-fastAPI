A01 = "A01"
C01 = "C01"
C02 = "C02"

error_codes: dict = {
    "A01": "idNotFound",
    "C01": "noteAlreadyCompleted",
    "C02": "noteNotCompletedYet"
}

def return_error(error_code, **kwargs):
    error_description = error_codes.get(error_code, None)
    if (error_description is None):
        raise KeyError(error_code)

    result = {
        "status": "KO",
        "code": error_code,
        "message": error_description
    }

    return {**result, **kwargs}
