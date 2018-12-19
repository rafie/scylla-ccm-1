
import re
import requests

class Prometheus():
    def __init__(self, ip='127.0.0.1', port=9180):
        self.ip = ip
        self.port = port
        self.url = 'http://{}:{}/metrics'.format(ip, port)
    
    # single entry: metrics['name'] == 17
    # multiple entries: metrics['name'] == [42, 43, 44]
    @property
    def metrics(self):
        return self.select()

    def select(self, names=[]):
        resp = requests.get(self.url)
        if resp.status_code not in [200, 201, 202]:
            raise 'Failed getting metrics from server {}:{}: {}'.format(self.ip, self.port, resp.content)
        lines = filter(lambda x: not x.startswith('#'), resp.content.splitlines())
        met = {}
        for line in lines:
            m = re.match('(\w*){([^}]*)}\s*(.*)', line)
            key = m.groups()[0]
            if names != [] and key not in names:
                continue
            val = m.groups()[2]
            try:
                val = int(val)
            except ValueError:
                val = float(val)
            if key not in met:
                met[key] = val
            elif isinstance(met[key], list):
                met[key].append(val)
            else:
                met[key] = [met[key], val]
        return met
