from locust import HttpUser, events, task, between
from locust.runners import MasterRunner
import requests

target_server_url = "http://127.0.0.1:8000"
data_server_url = "http://127.0.0.1:8080"

test_data = []
gen = None
def get_row():
    while True:
        for data in test_data:
            yield data

current_worker = None

@events.test_start.add_listener
def test_start(environment, **_kwargs):
    # happens only once in headless runs, but can happen multiple times in web ui-runs
    global test_data, gen, current_worker
    # in a distributed run, the master does not typically need any test data
    if not isinstance(environment.runner, MasterRunner):
        test_data = requests.get(f'{data_server_url}/get_chunk').json()
        gen = get_row()
        

class MyUser(HttpUser):
    host = target_server_url
    wait_time = between(2, 2)  

    @task
    def task1(self):
        data = next(gen)
        self.client.post("/task1", json=data)