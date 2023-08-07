from requests import Session
from grequests import send, get, put, delete, post
from consul import base


__all__ = ['Consul']

def _gsend(req):
    send(req).join()
    return req.response

class HTTPClient(base.HTTPClient):
    def __init__(self, *args, **kwargs):
        super(HTTPClient, self).__init__(*args, **kwargs)
        self.session = Session()

    def response(self, response):
        response.encoding = 'utf-8'
        return base.Response(
            response.status_code, response.headers, response.text)

    def get(self, callback, path, params=None):
        uri = self.uri(path, params)
        return callback(self.response(_gsend(get(uri, session=self.session, verify=self.verify, cert=self.cert))))

    def put(self, callback, path, params=None, data=''):
        uri = self.uri(path, params)
        return callback(self.response(_gsend(put(uri, session=self.session, data=data, verify=self.verify, cert=self.cert))))

    def delete(self, callback, path, params=None):
        uri = self.uri(path, params)
        return callback(self.response(_gsend(delete(uri, session=self.session, verify=self.verify, cert=self.cert))))

    def post(self, callback, path, params=None, data=''):
        uri = self.uri(path, params)
        return callback(self.response(_gsend(post(uri, session=self.session, data=data, verify=self.verify,
                              cert=self.cert))))


class Consul(base.Consul):
    def connect(self, host, port, scheme, verify=True, cert=None):
        return HTTPClient(host, port, scheme, verify, cert)
