import self
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import User

#
# class APITestCase:
#     pass


class TestSignup(TestCase):


    def setUp(self):
        self.url = reverse('register')

    def test_signup_returns_201(self):
        data = {
            "first_name": "Ebunoluwa",
            "last_name": "Collins",
            "email": "callebun24@gmail.com",
            "phone_number": "09043946021",
            "username": "Nemi243",
            "password": "Password123"
        }


        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_returns_400(self):
        data = {
            "first_name": "Ebunoluwa",
            "last_name": "Collins",
            "email": "callebun24.com",
            "phone_number": "09043946021",
            "username": "Nemi243",
            "password": "Pass"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestAuth(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "first_name": "Ebunoluwa",
            "last_name": "Collins",
            "email": "callebun24@gmail.com",
            "phone_number": "09043946021",
            "username": "Nemi243",
            "password": "Password123"
        }

    def test_signup_returns_201(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_data_returns_400(self):
        self.user_data = {
            "first_name": "Ebunoluwa",
            "last_name": "Collins",
            "email": "callebun24.com",
            "phone_number": "09043946021",
            "username": "Nemi243",
            "password": "Pass"
        }
        invalid_data = self.user_data.copy()
        invalid_data["email"] = "not-an-email"
        invalid_data["password"] = "short"

        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_200(self):

        self.client.post(self.register_url, self.user_data, format='json')


        login_data = {

            "first_name": "Ebunoluwa",
            "last_name": "Collins",
            "email": "callebun24@gmail.com",
            "phone_number": "09043946021",
            "username": "Nemi243",
            "password": "Password123"
        }


        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)