import re
from datetime import datetime


class FieldValidator():

    def __init__(self):
        self.__regular_expressions = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }

    # Run the validation for each field from the list
    def validate_fields(self, field_list):
        try:
            for field in field_list:
                validation_field = self.__validate_field(field)
                if validation_field["result"] is False:
                    return validation_field

            return self.__validation_response("Todos los campos son válidos")
        except Exception as e:
            raise Warning("Verifique la estructura de los datos e inténtelo"
                          + " nuevamente.") from e


    def __validate_field(self, field_data):
        # Get field info
        type_field = field_data.get("type")
        display_name = field_data.get("display_name")
        field_value = str(field_data.get("field_value", ""))
        required_field = field_data.get("required", False)
        limit = field_data.get("limit", -1)

        if limit != -1 and len(field_value) > limit:
            return self.__validation_response(
                f"El campo '{display_name}' debe contener como máximo {limit} caracteres.", False
            )

        if field_value == "" and required_field:
            return self.__validation_response(
                f'El campo "{display_name}" es requerido.', False
            )

        # Run type-specific validations
        validation_result = self.__run_type_specific_validation(type_field, field_value, display_name)
        return validation_result

    def __run_type_specific_validation(self, type_field, field_value, display_name):
        validation_functions = {
            "string": self.__validate_as_string,
            "int": self.__validate_as_integer,
            "alphanum": self.__validate_as_alphanum,
            "alphanum_ns": self.__validate_as_alphanum_no_spaces,
            "email": self.__validate_as_email,
            "float": self.__validate_as_float,
            "bit": self.__validate_as_bit,
            "date": self.__validate_as_date
        }

        if type_field in validation_functions:
            validation_function = validation_functions[type_field]
            validation_result = validation_function(field_value, display_name)
            if validation_result["result"] is False:
                return validation_result
        else:
            return self.__validation_response(
                f'El tipo de campo de "{display_name}" no es válido.', False
            )

        return self.__validation_response("El campo es válido.")

    # Evaluate a field value as STRING
    def __validate_as_string(self, value, display_name):
        if isinstance(value, str) is not True:
            return self.__validation_response(
                f'El campo "{display_name}" debe contener solo texto.',
                False
            )

        return self.__validation_response(
            f'El campo "{display_name}" es válido.'
        )

    # Evaluate a alphanum string without spaces
    def __validate_as_alphanum_no_spaces(self, value, display_name):
        check_alphanum = self.__validate_as_alphanum(value, display_name)
        if check_alphanum["result"] is False:
            return check_alphanum

        check_no_spaces = self.__validate_str_no_spaces(value, display_name)
        if check_no_spaces["result"] is False:
            return check_no_spaces

        return self.__validation_response(
                f'El campo "{display_name}" es válido.'
        )

    # Evalute strings without spaces
    def __validate_str_no_spaces(self, value, display_name):
        is_string = self.__validate_as_string(value, display_name)

        if is_string["result"] is False:
            return is_string

        if " " in value:
            return self.__validation_response(
                    f'El campo "{display_name}" no debe contener espacios.',
                    False
                )
        return self.__validation_response(
            f'El campo "{display_name}" es válido.'
        )

    # Evalute a field value as integer number
    def __validate_as_integer(self, value, display_name):
        try:
            int(value)
            if value == "" or value.isdigit() is not True:
                return self.__validation_response(
                    f'El campo "{display_name}" debe ser un número entero '
                    + 'positivo',
                    False
                )

            return self.__validation_response(
                f'El campo "{display_name}" es válido.'
            )
        except Exception:
            return self.__validation_response(
                f'El campo "{display_name}" debe ser un número entero '
                + 'positivo',
                False
            )

    # Evaluate a field value as date
    def __validate_as_date(self, value, display_name):
        format_amd = "%Y-%m-%d"
        try:
            bool(datetime.strptime(value, format_amd))
            return self.__validation_response(
                f'El campo "{display_name}" es válido.'
            )
        except ValueError:
            return self.__validation_response(
                    f'El campo "{display_name}" '
                    + 'debe ser una fecha en el formato YYYY-mm-dd',
                    False
                )

    # Evaluate a field value as float number
    def __validate_as_float(self, value, display_name):
        try:
            float_value = float(value)
            if isinstance(float_value, float) is False:
                return self.__validation_response(
                    f'El campo "{display_name}" no es válido.',
                    False
                )

            return self.__validation_response(
                f'El campo "{display_name}" es válido.'
            )
        except ValueError:
            return self.__validation_response(
                f'El campo "{display_name}" no es válido.',
                False
            )

    # Evalute a field value as ALPHANUMERIC
    def __validate_as_alphanum(self, value, display_name):

        validate_string = self.__validate_as_string(value, display_name)

        if validate_string["result"] is False:
            return validate_string

        value = value.replace(" ", "")

        if value != "" and value.isalnum() is False:
            return self.__validation_response(
                f'El campo "{display_name}" debe ser alfanumérico.',
                False
            )

        return self.__validation_response(
            f'El campo "{display_name}" es válido.'
        )

    # Evaluate a field value as BIT
    def __validate_as_bit(self, value, display_name):
        as_integer = self.__validate_as_integer(value, display_name)
        if as_integer["result"] is False or (value not in ("0", "1")):
            return self.__validation_response(
                f'El campo "{display_name}" debe ser un digito binario 0/1.',
                False
            )

        return self.__validation_response(
            f'El campo "{display_name}" es válido.'
        )

    # Evalute a field value as EMAIL
    def __validate_as_email(self, value, display_name):
        if re.fullmatch(self.__regular_expressions["email"],
                        value) is None:
            return self.__validation_response(
                f'El campo "{display_name}" no es válido.',
                False
            )

        return self.__validation_response(
            f'El campo "{display_name}" es válido.'
        )

    # Build a format_amd response for the validations
    def __validation_response(self, message, result=True):
        return {"message": message, "result": result}
