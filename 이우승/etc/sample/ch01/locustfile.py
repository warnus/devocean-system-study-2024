from locust import HttpUser, between, task

class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def calculate_fibonacci(self):
        self.client.get("/fibonacci/random")
    
    # @task
    # def get_employees(self):
    #     self.client.get("/employees/")
    
    # @task
    # def get_employees(self):
    #     self.client.get("/multi/employees/")