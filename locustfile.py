import random
from locust import HttpUser, task, between

class TinyInstaUser(HttpUser):
    # Simulate a user thinking for 1-2 seconds between requests
    wait_time = between(1, 2)

    @task
    def view_timeline(self):
        """
        Simulates a user requesting their timeline via the API.
        """
        user_num = random.randint(1, 1000)
        user_id = f"user{user_num}"
        self.client.get(f"/api/timeline?user={user_id}", name="/api/timeline")
