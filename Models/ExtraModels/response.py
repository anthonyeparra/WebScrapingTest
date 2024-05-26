import json
import datetime


class Response():

    def __init__(
            self, name: str, message: str = "", data: dict = [], excep=None
    ):
        self.excep = excep
        self.__prepare_body(name, message)
        self.data = data if isinstance(data, list) else [data]

    # Build a internal format response
    def __prepare_body(self, name: str, message: str = ""):

        if name == "ENTITY_ERROR":
            self.code = 422
            self.message = f"No se pudo obtener el valor del campo {message}."
        elif name == "BAD_REQ":
            self.code = 400
            if message == "":
                self.message = "Ha ocurrido un error al procesar los datos."
            else:
                self.message = message
        elif name == "INTERNAL_ERROR":
            self.code = 500
            self.message = "Ha ocurrido un error inesperado."
        elif name == "OK_CREATE":
            self.code = 201
            self.message = "El registro ha sido exitoso."
        elif name == "OK_UPDATE":
            self.code = 201
            self.message = "La actualización ha sido exitosa."
        elif name == "OK":
            self.code = 200
            self.message = "Operación exitosa."
        elif name == "BAD_CRED":
            self.code = 403
            self.message = "Acceso no permitido."

    # Return a format lambda response
    def to_lambda_response(self):

        internal_reponse = {
            "status": self.code,
            "message": self.message,
            "data": self.data
        }

        api_response = {
            "statusCode": self.code,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,'
                + 'UPDATE,DELETE',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With,'
                + ' Content-Type, Accept'
            },
            "body": json.dumps(internal_reponse, default=myconverter)
        }
        # Muestre de error por consola
        if self.code not in [200, 201]:
            if self.excep:
                print("¡Error! ", str(self.excep))
            else:
                print("¡Error Controlado! ", self.message)

        return api_response


def myconverter(o):

    if isinstance(o, datetime.date):
        return o._str_()
