C01 = "C01"
C02 = "C02"

error_codes: dict = {
    "C01": "Trying to complete a note already set to completed",
    "C02": "Trying to set as not complete a note not completed yet"
}

def return_error(error_code):
    error_description = error_codes.get(error_code, None)
    if (error_description is None):
        raise KeyError(error_code)

    return {
        "status": "KO",
        "code": error_code,
        "message": error_description
    }
