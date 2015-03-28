import json

from django.http import HttpResponse


class JSONResponse(HttpResponse):

    def __init__(self, data):
        HttpResponse.__init__(
            self, content=json.dumps(data), content_type='application/json')

