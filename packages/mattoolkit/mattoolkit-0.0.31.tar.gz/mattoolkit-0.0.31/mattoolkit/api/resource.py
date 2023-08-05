import requests

from .api import api, MTKAPIError


class Resource:
    api = api

    @property
    def url(self):
        return self.api.API_ROOT + '/' + self.resource


class ResourceList(Resource):
    ITEM = None

    def __init__(self, resource):
        self.resource = resource
        self.items = []

    def convert_item(self, item):
        if self.ITEM is None:
            raise NotImplementedError('Must declare item version of list')

        resource_item = self.ITEM(0)
        resource_item.id = item['id']
        resource_item.data = item
        return resource_item

    def get(self, params=None, request_all=True):
        params = params or {}
        response = self.api.session.get(self.url, params=params)
        if response.status_code != 200:
            raise MTKAPIError(response.status_code, response.text)

        self.items = []
        response_json = response.json()
        self.items.extend([self.convert_item(item) for item in response_json['data']])

        if request_all:
            offset = response_json['metadata']['offset']
            total = response_json['metadata']['total']
            limit = response_json['metadata']['limit']
            for _offset in range(offset + limit, total, limit):
                params['offset'] = _offset
                response = self.api.session.get(self.url, params=params)
                if response.status_code != 200:
                    raise MTKAPIError(response.status_code, response.text)

                response_json = response.json()
                self.items.extend([self.convert_item(item) for item in response_json['data']])

    def query(self, **kwargs):
        self.get(params=kwargs)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n'.join(map(str, self.items))


class ResourceItem(Resource):
    def __init__(self, resource, id):
        self.resource = resource
        self.id = None if id is None else int(id)
        self.data = None

    def __eq__(self, other):
        if type(self) is type(other) and \
           self.resource == other.resource and self.id == other.id:
            return True
        return False

    def get(self):
        response = self.api.session.get(self.url + '/' + str(self.id))
        if response.status_code != 200:
            raise MTKAPIError(response.status_code, response.text)
        self.data = (response.json())['data']

    def save(self):
        if self.id:
            response = self.api.session.put(self.url + '/' + str(self.id), json=self.data)
        else:
            response = self.api.session.post(self.url, json=self.data)
        if response.status_code != 200:
            raise MTKAPIError(response.status_code, response.text)
        self.data = (response.json())['data']
        self.id = self.data['id']

    def delete(self):
        response = self.api.session.delete(self.url + '/' + str(self.id))
        if response.status_code != 200:
            raise MTKAPIError(response.status_code, response.text)

    def __repr__(self):
        return f'<{self.__class__.__name__}: resource: {self.resource}, id: {self.id}>'
