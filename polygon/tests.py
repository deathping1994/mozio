import json
from django.test.client import Client
from django.test import TestCase
from mongoengine import *
from .models import Provider
import pymongo


class TestCalls(TestCase):
    def setUp(self):
        """Initialize the django test client"""
        self.client = Client()

    def test_call_provider_inserts_provider(self):
        response = self.client.post('/provider/', {"name":"test",
                                                   "email":"test@gmail.com",
                                                   "phone":"+918375847",
                                                   "currency":"inr",
                                                   "lang":"eng"},content_type="application/json")
        provider = Provider.objects(email="test@gmail.com")
        self.assertEquals(provider.to_json(),response.json())

    def test_call_search_gives_intersecting_polygons(self):
        response = self.client.get('/search/?lat=1&&long=1')
        self.assertEquals(len(response.json()),1)

    def tearDown(self):
        pass

def get_db():
    """ GetDB - simple function to wrap getting a database
    connection from the connection pool.
    """
    conn = pymongo.MongoClient()
    return conn.mozio


class ProviderMethodTests(TestCase):

    def setUp(self):
        self.db = get_db()

    def test_create_provider(self):
        """
        create method should create a Provider object and insert
        it in mongodb
        """
        provider = Provider("test","test123@gmail.com","+918375847","inr")
        provider.save()
        self.assertIsInstance(provider,Provider,"Instance created")
        res=Provider.objects(email="test123@gmail.com").to_json()
        self.assertEquals(Provider.objects.get(pk=provider.id).to_json(),res)

    def test_delete_provider(self):

        """
        Tests if the objects are getting deleted by deleting
        the object created in previous test
        """
        provider = Provider.objects(email="test123@gmail.com")
        provider.delete()
        res = False
        try:
            provider = Provider.objects(email="test123@gmail.com")
        except Exception as e:
            self.assertIsInstance(e,DoesNotExist)

    def tearDown(self):
        try:
            provider = Provider.objects(email= "test123@gmail.com")
            provider.delete()
        except DoesNotExist:
            pass