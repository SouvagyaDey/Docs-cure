"""
Locust load test for DocsCure API.
Simulates 1,000+ concurrent users hitting the application.
"""

import random
import string
from locust import HttpUser, task, between, events


class HealthCheckUser(HttpUser):
    """Lightweight user that only hits the health endpoint — 10% of traffic."""
    weight = 1

    wait_time = between(1, 3)

    @task
    def health(self):
        self.client.get("/api/auth/health/", name="/health")


class AnonymousBrowsingUser(HttpUser):
    """Simulates unauthenticated users browsing public endpoints — 50% of traffic."""
    weight = 5

    wait_time = between(1, 5)

    @task(5)
    def list_products(self):
        self.client.get("/api/products/product/", name="/products/list")

    @task(3)
    def get_product_detail(self):
        product_id = random.randint(1, 21)
        self.client.get(f"/api/products/product/{product_id}/", name="/products/detail")

    @task(4)
    def list_doctors(self):
        self.client.get("/api/doctorappointment/doctors/", name="/doctors/list")

    @task(2)
    def get_doctor_detail(self):
        doctor_id = random.randint(1, 5)
        self.client.get(f"/api/doctorappointment/doctors/{doctor_id}/", name="/doctors/detail")

    @task(3)
    def list_hospitals(self):
        self.client.get("/api/hospitalmanagement/hospitals/", name="/hospitals/list")

    @task(2)
    def list_product_stores(self):
        self.client.get("/api/products/productstore/", name="/productstores/list")

    @task(2)
    def list_doctor_reviews(self):
        self.client.get("/api/doctorappointment/doctor_reviews/", name="/doctor_reviews/list")

    @task(1)
    def list_profiles(self):
        self.client.get("/api/profiles/", name="/profiles/list")


class AuthenticatedUser(HttpUser):
    """Simulates logged-in users performing authenticated actions — 40% of traffic."""
    weight = 4

    wait_time = between(2, 6)

    def on_start(self):
        """Register a new user and log in."""
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.email = f"loadtest_{suffix}@test.com"
        self.password = "TestPass123!"
        self.username = f"loadtester_{suffix}"

        # Register
        resp = self.client.post(
            "/api/auth/signup/",
            json={
                "email": self.email,
                "password": self.password,
                "username": self.username,
                "first_name": "Load",
                "last_name": "Tester",
            },
            name="/auth/signup",
        )

        # Login
        resp = self.client.post(
            "/api/auth/login/",
            json={"email": self.email, "password": self.password},
            name="/auth/login",
        )

    @task(5)
    def browse_products(self):
        self.client.get("/api/products/product/", name="/products/list")

    @task(3)
    def browse_doctors(self):
        self.client.get("/api/doctorappointment/doctors/", name="/doctors/list")

    @task(2)
    def get_current_user(self):
        self.client.get("/api/auth/user/", name="/auth/user")

    @task(2)
    def check_auth_status(self):
        self.client.get("/api/auth/isauthenticated/", name="/auth/isauthenticated")

    @task(1)
    def browse_cart(self):
        self.client.get("/api/cart/", name="/cart/list")

    @task(1)
    def browse_orders(self):
        self.client.get("/api/orders/orders/", name="/orders/list")
