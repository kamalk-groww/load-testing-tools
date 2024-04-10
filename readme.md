## Setup

##### Create a virtual environment

```bash
python3 -m venv env
```


##### Activate the virtual environment

```bash
source env/bin/activate
```

##### Install dependencies

```bash
pip3 install -r requirements.txt
```

### Guide
- Spin the dataserver
- Add the following at top of your loadtest file
```python
from locust.runners import MasterRunner
from locust import events
import requests

target_server_url = "http://127.0.0.1:8000"
data_server_url = "http://127.0.0.1:8080"

test_data = []
gen = None
def get_row():
    while True:
        for data in test_data:
            yield data

@events.test_start.add_listener
def test_start(environment, **_kwargs):
    # happens only once in headless runs, but can happen multiple times in web ui-runs
    global test_data, gen, current_worker
    # in a distributed run, the master does not typically need any test data
    if not isinstance(environment.runner, MasterRunner):
        test_data = requests.get(f'{data_server_url}/get_chunk').json() # get data
        gen = get_row() # initialise the generator
```
- Example User
```python
class MyUser(HttpUser):
    host = target_server_url
    wait_time = between(2, 2)  

    @task
    def task1(self):
        data = next(gen) # gets the row from the test_data
        self.client.post("/task1", json=data)
```

##### Run the dataserver

Define filename, chunksize in dataserver.py
```bash
uvicorn dataserver:app --port 8080
```