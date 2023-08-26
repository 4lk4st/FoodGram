import json

from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


from .models import FoodUser


class AccountCreationTests(APITestCase):

    def setUp(self):
        self.user_info = {
            'email': 'test@test.com',
            'username': 'testname',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'testpassword123!'
        }

    def test_user_creation_in_db(self):
        """
        Проверяем что user с нужными полями создается в базе.
        """
        FoodUser.objects.create_user(**self.user_info)
        self.assertEqual(FoodUser.objects.count(), 1)
        self.assertEqual(FoodUser.objects.get().email, self.user_info['email'])
        self.assertEqual(FoodUser.objects.get().username, self.user_info['username'])
        self.assertEqual(FoodUser.objects.get().first_name, self.user_info['first_name'])
        self.assertEqual(FoodUser.objects.get().last_name, self.user_info['last_name'])

    def test_create_account(self):
        """
        Проверяем, что мы можем создавать новый аккаунт через api.
        """
        url = 'http://127.0.0.1:8000/api/users/'
        response = self.client.post(url, self.user_info, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodUser.objects.count(), 1)
        self.assertEqual(FoodUser.objects.get().email, self.user_info['email'])
        self.assertEqual(FoodUser.objects.get().username, self.user_info['username'])
        self.assertEqual(FoodUser.objects.get().first_name, self.user_info['first_name'])
        self.assertEqual(FoodUser.objects.get().last_name, self.user_info['last_name'])


class AccountEndpointTests(APITestCase):

    def setUp(self):
        self.user_info = {
            'email': 'test@test.com',
            'username': 'testname',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'testpassword123!'
        }

        url = 'http://127.0.0.1:8000/api/users/'
        self.new_user = self.client.post(url, self.user_info, format='json')

    def test_user_list(self):
        """
        Проверяем, что мы видим user-list через api.
        """
        url = 'http://127.0.0.1:8000/api/users/'

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", json.loads(response.content))
        self.assertIn("next", json.loads(response.content))
        self.assertIn("previous", json.loads(response.content))
        self.assertIn("results", json.loads(response.content))
        self.assertEqual(json.loads(response.content)['results'][0]["email"], json.loads(self.new_user.content)["email"])
        self.assertEqual(json.loads(response.content)['results'][0]["id"], json.loads(self.new_user.content)["id"])
        self.assertEqual(json.loads(response.content)['results'][0]["username"], json.loads(self.new_user.content)["username"])
        self.assertEqual(json.loads(response.content)['results'][0]["first_name"], json.loads(self.new_user.content)["first_name"])
        self.assertEqual(json.loads(response.content)['results'][0]["last_name"], json.loads(self.new_user.content)["last_name"])
        self.assertNotIn("password", json.loads(response.content))

    def test_user_profile_by_id(self):
        """
        Проверяем, что можно видеть профиль любого пользователя по id
        """

        url = 'http://127.0.0.1:8000/api/users/1/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["email"], json.loads(self.new_user.content)["email"])
        self.assertEqual(json.loads(response.content)["id"], json.loads(self.new_user.content)["id"])
        self.assertEqual(json.loads(response.content)["username"], json.loads(self.new_user.content)["username"])
        self.assertEqual(json.loads(response.content)["first_name"], json.loads(self.new_user.content)["first_name"])
        self.assertEqual(json.loads(response.content)["last_name"], json.loads(self.new_user.content)["last_name"])
        self.assertNotIn("password", json.loads(response.content))
    
    def test_user_own_profile(self):
        """
        Проверяем доступность профиля текущего пользователя
        """
        data = {
            "password": self.user_info['password'],
            "email": self.user_info['email']
        }
        self.client.post('http://127.0.0.1:8000/api/auth/token/login/',
                         data, format='json')
        token = Token.objects.get(user__username=self.user_info['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = 'http://127.0.0.1:8000/api/users/me/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["email"], json.loads(self.new_user.content)["email"])
        self.assertEqual(json.loads(response.content)["id"], json.loads(self.new_user.content)["id"])
        self.assertEqual(json.loads(response.content)["username"], json.loads(self.new_user.content)["username"])
        self.assertEqual(json.loads(response.content)["first_name"], json.loads(self.new_user.content)["first_name"])
        self.assertEqual(json.loads(response.content)["last_name"], json.loads(self.new_user.content)["last_name"])
        self.assertNotIn("password", json.loads(response.content))

    def test_user_reset_password(self):
        """
        Проверяем возможность смены пароля через api
        """
        new_user = self.client.post('http://127.0.0.1:8000/api/users/',
                                    self.user_info, format='json')
        
        data = {
            "password": self.user_info['password'],
            "email": self.user_info['email']
        }
        self.client.post('http://127.0.0.1:8000/api/auth/token/login/',
                         data, format='json')
        token = Token.objects.get(user__username=self.user_info['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {
            "new_password": "new_test_password",
            "current_password": self.user_info['password']
        }
        
        url = 'http://127.0.0.1:8000/api/users/set_password/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(check_password(data['new_password'], FoodUser.objects.get().password))


class AuthEndpointTests(APITestCase):

    def setUp(self):
        self.user_info = {
            'email': 'test@test.com',
            'username': 'testname',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'testpassword123!'
        }

        url = 'http://127.0.0.1:8000/api/users/'
        self.new_user = self.client.post(url, self.user_info, format='json')
    
    def test_get_token(self):
        """
        Проверяем возможность получения токена авторизации
        """       
        data = {
            "password": self.user_info['password'],
            "email": self.user_info['email']
        }

        url = 'http://127.0.0.1:8000/api/auth/token/login/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(json.loads(response.content)["auth_token"])
    
    def test_delete_token(self):
        """
        Проверяем возможность удаления токена авторизации
        """
        data = {
            "password": self.user_info['password'],
            "email": self.user_info['email']
        }
        self.client.post('http://127.0.0.1:8000/api/auth/token/login/',
                         data, format='json')
        
        token = Token.objects.get(user__username=self.user_info['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
 
        url = 'http://127.0.0.1:8000/api/auth/token/logout/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
