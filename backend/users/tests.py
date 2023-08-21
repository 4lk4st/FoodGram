from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FoodUser

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('api-users')
        data = {
            'email': 'test@test.com',
            'username': 'testname',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'testpassword123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodUser.objects.count(), 1)
        self.assertEqual(FoodUser.objects.get().email, 'test@test.com')
