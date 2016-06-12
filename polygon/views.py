from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from models import Provider
from mongoengine import *
from error import *
from . import db, json_response
from bson import ObjectId, json_util
import json

def test(request):
    """Random function to test if django setup working"""
    provider = Provider.objects.all()
    print provider
    res= {"re":"dsd"}
    return json_response(json.dumps(res),200)


@csrf_exempt
def service_provider(request, id= ''):
    """
        endpoint: /provider/<id>/
        method: GET
        response: Service provider object stored in Database
        method: Post
        body: Json (name,email,phone,currency)
        response: 201, Newly created Service provider object
        method: Put
        body: Json (name,email,phone,currency)
        response: 200, Updated Service Provider Object
        method: Delete
        response: 204, No content
        ________________________________________________________________________________________
        endpoint: /provider/all
        method: GET
        response: Array of all service provider objects
    """
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            provider = Provider(name=data['name'], email=data['email'], phone=data['phone'],
                                currency=data['currency'],service_area=[])
            provider.save()
            return json_response(provider.to_json(), 201)
        if request.method == "GET":
            if id is None or id == '':
                providers= Provider.objects.all()
                return json_response(providers.to_json(), 200)
            else:
                provider = Provider.objects.get(pk=id)
                return json_response(provider.to_json(), 200)
        provider = Provider.objects.get(pk=id)
        if request.method == "PUT":
            data = json.loads(request.body)
            provider.name = data['name']
            provider.email = data['email']
            provider.phone = data['phone']
            provider.currency = data['currency']
            provider.save()
            return json_response(provider.to_json(), 200)
        if request.method == "DELETE":
            provider.delete()
            return json_response('',204)
    except Exception as e:
        response = error_handler(e)
        return response


@csrf_exempt
def update_service_area(request,id):
    """
        endpoint: /provider/<id>/area/
        method: GET
        response: Service area of service provider with id passes in url
        method: Post
        body: Json (service_area: <array of valid polygon line strings>)
        response: 200, Updated Service provider object
        method: Put
        body: Json (service_area: <line strings to add in existing polygon>)
        response: 200, Updated Service Provider Object
        method: Delete
        body: Json(service_area: <line strings to delete from polygon>)
        response: 200, Updated Service provider object with one line string removed
        ________________________________________________________________________________________
    """
    try:
        provider = Provider.objects.get(pk=id)
        if request.method == "GET":
            return json_response(json.dumps(provider.service_area), 200)
        data= json.loads(request.body)
        if request.method == "POST":
            provider.service_area = []
            for poly in data['service_area']:
                provider.service_area.append(poly)
            provider.save()
            return json_response(provider.to_json(), 201)

        elif request.method == "PUT":
            for poly in data['service_area']:
                provider.service_area.append(poly)
            provider.save()
            return json_response(provider.to_json(), 200)
        elif request.method == "DELETE":
            for poly in data['service_area']:
                poly = {"type":"Polygon","coordinates":poly}
                if poly in provider.service_area:
                    provider.service_area.remove(poly)
            provider.save()
            return json_response(provider.to_json(), 200)
        else:
            raise MethodError("Allowed Method: POST,PUT,DELETE")
    except Exception as e:
        return error_handler(e)


@cache_page(60 * 15)        #Cache response in Redis for 15 minutes
@csrf_exempt
def search(request):
    try:
        if request.method == "GET":
            lat = request.GET.get("lat")
            long = request.GET.get("long")
            providers = Provider.objects(__raw__={
                            "service_area": {
                                    "$geoIntersects": {
                                        "$geometry": {
                                          "type": "Point" ,
                                          "coordinates": [float(lat), float(long)]
                                        }

                                    }}})
            return json_response(providers.to_json(),200)
        else:
            response = dict()
            response['error'] = "Allowed Methods: GET"
            return json_response(json.dumps(response),400)
    except Exception as e:
        return error_handler(e)

