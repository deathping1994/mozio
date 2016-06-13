from __future__ import unicode_literals
from django.utils.html import strip_tags, escape
from mongoengine import *
import re
# Create your models here.


class Provider(Document):
    name = StringField(max_length=30)
    email = EmailField(unique=True)
    phone = StringField(max_length=13)
    lang = StringField()
    currency = StringField(max_length=10)
    service_area = MultiPolygonField()

    meta = {'allow_inheritance': True}


    def clean(self):
        msg_list = list()
        self.name = escape(strip_tags(self.name))
        if not re.match("\+[0-9]*", self.phone):
            msg_list.append("Valid phone number begins with + followed by country code and phone number")
            raise ValidationError(",".join(msg_list))


