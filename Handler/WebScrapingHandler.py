from Models.ExtraModels.response import Response
from Helpers.basic_helper import get_json_data
from Utils.decorators import give_response
from Class.WebScraping import WebScraping

@give_response
def get_information_cufe(event, context):
    request_body = get_json_data(event["body"])
    web_scraping = WebScraping()
    res = web_scraping.get_information_cufe(request_body)
    return Response("OK",data=res)

