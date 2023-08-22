import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FoodUser

class AccountTests(APITestCase):

    def setUp(self):
        self.user_info = {
            'email': 'test@test.com',
            'username': 'testname',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'testpassword123!'
        }

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = 'http://127.0.0.1:8000/api/users/'
        response = self.client.post(url, self.user_info, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodUser.objects.count(), 1)
        self.assertEqual(FoodUser.objects.get().email, 'test@test.com')
        self.assertEqual(FoodUser.objects.get().username, 'testname')
        self.assertEqual(FoodUser.objects.get().first_name, 'test_first_name')
        self.assertEqual(FoodUser.objects.get().last_name, 'test_last_name')

    def test_user_list(self):
        """
        Ensure we can view user's list with fresh user
        """
        url = 'http://127.0.0.1:8000/api/users/'
        new_user = self.client.post(url, self.user_info, format='json')
        self.assertEqual(new_user.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodUser.objects.count(), 1)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])
        self.assertEqual(json.loads(response.content)[0]["email"], json.loads(new_user.content)["email"])
        self.assertEqual(json.loads(response.content)[0]["username"], json.loads(new_user.content)["username"])
