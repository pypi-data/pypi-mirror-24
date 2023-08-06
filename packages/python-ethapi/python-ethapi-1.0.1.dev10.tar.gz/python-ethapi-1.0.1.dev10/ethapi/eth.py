import requests
import json


class Eth(object):
    def __init__(self, **kwargs):
        self.user_agent = 'python-ethapi'
        try:
            self.endpoint = kwargs['endpoint']
        except KeyError:
            raise KeyError('Ethermine API endpoint is required')

        self.miner_id = kwargs.get('miner_id', None)
        self.worker_id = kwargs.get('worker_id', None)
        self.timeout = kwargs.get('timeout', None)
        self.verify = kwargs.get('verify', None)
        self.pagination = kwargs.get('pagination', False)
        self.http = requests.Session()

    def _request(self, url, method, **kwargs):
        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        if self.verify is not None:
            kwargs.setdefault('verify', self.verify)

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = self.user_agent
        kwargs['headers']['Accept'] = 'application/json'
        kwargs['headers']['Content-Type'] = 'application/json'

        # If we're sending data, make sure it's json encoded
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        resp = self.http.request(method, url, **kwargs)
        if not resp.ok:
            resp.raise_for_status()

        try:
            body = resp.json()
        except ValueError:
            body = None

        if not self.pagination:
            if body is not None and 'meta' in body and 'pagination' in body['meta']:
                page_info = body['meta']['pagination']
                if page_info['total'] > page_info['count']:
                    # There are items not displayed in our result
                    kwargs.setdefault('params', kwargs.get('params', {}))
                    kwargs['params']['per_page'] = page_info['total']
                    return self._request(url, method, **kwargs)

        return resp, body

    def _get(self, path, **kwargs):
        url = "%s/%s" % (self.endpoint, path)
        response, data = self._request(url, 'GET', **kwargs)
        return json.dumps(data, indent=2)
