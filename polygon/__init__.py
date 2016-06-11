from pymongo import MongoClient
from django.http import HttpResponse
client = MongoClient('localhost',27017)
db = client.mozio


def json_response(response,status):
    return HttpResponse(response, content_type="application/json", status=status)

