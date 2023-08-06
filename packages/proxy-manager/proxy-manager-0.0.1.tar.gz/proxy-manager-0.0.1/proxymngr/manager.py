import random
import threading

class ProxyManager(object):
    def __init__(self, proxy_file_path):
        self.proxies = self.load_proxies_from_file(proxy_file_path)
        self.lock = threading.Lock()
        self.proxy_number = 0
        
    @staticmethod
    def load_proxies_from_file(proxy_file_path):
        proxies = []
        with open(proxy_file_path) as proxy_file:
            for line in proxy_file.readlines():
                split_line = line.strip('\n').split(':')

                ip = split_line[0]
                port = split_line[1]
                proxy = '{0}:{1}'.format(ip, port)

                # If has username/password
                if len(split_line) == 4:
                    username = split_line[2]
                    password = split_line[3]
                    proxy = '{0}:{1}@{2}'.format(username, password, proxy)
                
                proxies.append({
                    'http': 'http://{}'.format(proxy),
                    'https': 'https://{}'.format(proxy)
                })
        return proxies

    def random_proxy(self):
        return random.choice(self.proxies)

    def next_proxy(self):
        if self.proxy_number >= len(self.proxies):
            self.proxy_number = 0

        with self.lock:
            proxy = self.proxies[self.proxy_number]
            self.proxy_number += 1
            return proxy
            