from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from .models import User

from rest_framework import status

# Create your tests here.

class TestSignup(TestCase):
    # def test_signup_returns_201(self):
    #     url = reverse("register")
    #     data = {
    #         "first_name": "Achalugo",
    #         "last_name": "Chiamie",
    #         "email": "chiedoziegochiamaka@gmail.com",
    #         "phone": "08101235568",
    #         "username": "Chimasky",
    #         "password": "helix456",
    #     }
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.url = reverse("register")
        self.login_url = reverse("login")
        self.data = {
            "first_name": "Achalugo",
            "last_name": "Chiamie",
            "email": "chiedoziegochiamaka@gmail.com",
            "phone": "08101235568",
            "username": "Chimasky",
            "password": "helix456",
        }
        self.login_data = {
            "email": "chiedoziegochiamaka@gmail.com",
            "password": "helix456"
        }

    def test_signup_returns_201(self):

        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_returns_400(self):
        data = {
            "first_name": "Achalugo",
            "last_name": "Chiamie",
            "email": "chiedoziegochiamaka.com",
            "phone": "08101235568",
            "username": "Chimasky",
            "password": "helix456",
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_login_returns_200(self):
        self.client.post(self.url, self.data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_details_returns_400(self):
        self.client.post(self.url, self.data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)