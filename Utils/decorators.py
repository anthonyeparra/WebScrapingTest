from Models.ExtraModels.response import Response
import traceback

# ExceptionHandler Decorator for lambda functions
def give_response(function_to_run):

    def wrapper(*args, **kwargs):
        try:
            response = function_to_run(*args, **kwargs)
        except KeyError as ke:
            error_log(ke)
            response = Response("ENTITY_ERROR", str(ke))
        except Warning as wa:
            error_log(wa)
            response = Response("BAD_REQ", str(wa))
        except ValueError as ve:
            error_log(ve)
            response = Response("BAD_REQ", str(ve))
        except TypeError as te:
            error_log(te)
            response = Response("BAD_REQ")
        except Exception as e:
            error_log(e)
            response = Response("INTERNAL_ERROR")
        try:
            return response.to_lambda_response()
            
        except Exception as e:
            response = Response("INTERNAL_ERROR", excep=e)
            lambda_response = response.to_lambda_response()
            
        return lambda_response

    return wrapper

def error_log(e):
    print(str(e))
    print(traceback.extract_tb(e.__traceback__))