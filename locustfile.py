'''
A small file to run some load tests.

The first task tries to short an URL to a query on google search,
creating 9 types of URLs randomly.

The second one tries to access them randomly. Some failures can happen 
when it tries to access the URLs before creating them or
when the amount of requests is rejected
by external servers because of the number of requests per second.

Disable the second task if you want to test the machine 
without relying on the network.
'''

from locust import HttpLocust, TaskSet, task
import random

myheaders = {'Content-Type': 'application/json', 'Accept': 'application/json'};

class UserBehavior(TaskSet):
    @task(1)
    def short_url(self):
        jsonData = '{"url":"https://www.google.com/search?q=number+' + str(random.randint(1, 9)) + '"}';
        self.client.post("/shorten_url", data = jsonData, headers = myheaders);
    
    @task(2)
    def access_shortened_url(self):
        id = str(random.randint(1, 9));
        self.client.get("/" + id);


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000