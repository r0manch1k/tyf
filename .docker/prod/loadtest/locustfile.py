from locust import HttpUser, task, between


class LoadTesterUser(HttpUser):
    WAIT_TIME = between(1, 2)

    @task
    def load_main_page(self):
        self.client.get("/")
