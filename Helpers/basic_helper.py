import json
# Apply strip function to specified field values
def apply_strip_fields(data: dict, fields_strip: tuple):
    for key in fields_strip:
        if type(data[key]) is not str:
            raise ValueError(f"El valor del atributo '{key}' es incorrecto.")

        data[key] = " ".join(data[key].split())

    return data

# Get json data and catch errors
def get_json_data(json_string: str):
    try:
        return json.loads(json_string)
    except Exception as ve:
        raise ValueError(
            "Verifique los datos de entrada e inténtelo nuevamente."
        ) from ve
    
# Get data for request
def dict_data(form_token, recaptcha_token, dato_):
    return {
        "__RequestVerificationToken": form_token,
        "RecaptchaToken": recaptcha_token,
        "DocumentKey": dato_
    }

