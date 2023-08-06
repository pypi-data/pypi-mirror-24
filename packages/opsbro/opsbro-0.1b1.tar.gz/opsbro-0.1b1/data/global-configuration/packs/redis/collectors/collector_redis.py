import time
import socket

from opsbro.collector import Collector
from opsbro.parameters import StringParameter, IntParameter


# Parse the result of Redis's INFO command into a Python dict
def parse_info(response):
    info = {}
    
    
    def get_value(value):
        if ',' not in value or '=' not in value:
            try:
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                return value
        else:
            sub_dict = {}
            for item in value.split(','):
                k, v = item.rsplit('=', 1)
                sub_dict[k] = get_value(v)
            return sub_dict
    
    
    for line in response.splitlines():
        if line and not line.startswith('#'):
            if line.find(':') != -1:
                key, value = line.split(':', 1)
                info[key] = get_value(value)
            else:
                # if the line isn't splittable, append it to the "__raw__" key
                info.setdefault('__raw__', []).append(line)
    
    return info


class Redis(Collector):
    RATE_KEYS = ['used_cpu_sys', 'used_cpu_sys_children', 'used_cpu_user', 'used_cpu_user_children',
                 'total_commands_processed']
    
    parameters = {
        'server'  : StringParameter(default='127.0.0.1'),
        'port'    : IntParameter(default=6379),
    }

    
    def __init__(self):
        super(Redis, self).__init__()
        self.store = {}
        self.last_launch = 0.0
    
    
    def launch(self):
        addr = '127.0.0.1'
        port = 6379
        logger = self.logger
        
        start = time.time()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((addr, port))
            s.send('INFO\n')
            buf = s.recv(8096)
            s.close()
        except Exception, exp:
            logger.debug('Cannot connect to redis at %s:%d : %s' % (addr, port, exp))
            return {'available': False}
        info = parse_info(buf)
        
        now = int(time.time())
        diff = now - self.last_launch
        self.last_launch = now
        
        latency_ms = round((time.time() - start) * 1000, 2)
        info['connexion_latency_ms'] = latency_ms
        info['available'] = True
        
        to_add = {}
        for (k, v) in info.iteritems():
            if k in self.RATE_KEYS:
                if k in self.store:
                    to_add['%s/s' % k] = (v - self.store[k]) / diff
                else:
                    to_add['%s/s' % k] = 0
                self.store[k] = info[k]
        
        for k in self.RATE_KEYS:
            del info[k]
        info.update(to_add)
        
        return info
