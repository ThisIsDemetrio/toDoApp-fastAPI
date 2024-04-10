# TODO: error_codes should move on its own file
A01 = "A01"
A02 = "A02"
C01 = "C01"
C02 = "C02"
C03 = "C03"
U00 = "U00"
Y00 = "Y00"

# TODO: this should be called error map
error_codes: dict = {
    "A01": "idNotFound",
    "A02": "dateNotValid",
    "C01": "todoAlreadyCompleted",
    "C02": "todoNotCompletedYet",
    "C03": "remainderNotFound",
    "U00": "unhandledException",
    "Y00": "usernameAlreadyTaken",
}

def return_error(error_code, **kwargs):
    error_description = error_codes.get(error_code, None)
    if (error_description is None):
        raise KeyError(error_code)

    # TODO: This should be a model
    result = {
        "status": "KO",
        "code": error_code,
        "message": error_description
    }

    return {**result, **kwargs}
