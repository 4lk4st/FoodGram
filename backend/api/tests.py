import json
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from recipes.models import Tag, Ingredient
from users.models import FoodUser


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
        self.assertEqual(FoodUser.objects.get().email,
                         self.user_info['email'])
        self.assertEqual(FoodUser.objects.get().username,
                         self.user_info['username'])
        self.assertEqual(FoodUser.objects.get().first_name,
                         self.user_info['first_name'])
        self.assertEqual(FoodUser.objects.get().last_name,
                         self.user_info['last_name'])

    def test_create_account(self):
        """
        Проверяем, что мы можем создавать новый аккаунт через api.
        """
        url = 'http://127.0.0.1:8000/api/users/'
        response = self.client.post(url, self.user_info, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodUser.objects.count(), 1)
        self.assertEqual(FoodUser.objects.get().email,
                         self.user_info['email'])
        self.assertEqual(FoodUser.objects.get().username,
                         self.user_info['username'])
        self.assertEqual(FoodUser.objects.get().first_name,
                         self.user_info['first_name'])
        self.assertEqual(FoodUser.objects.get().last_name,
                         self.user_info['last_name'])


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
        self.new_user = self.client.post(url,
                                         self.user_info, format='json')

    def test_user_profile_by_id(self):
        """
        Проверяем, что можно видеть профиль любого пользователя по id
        """

        url = 'http://127.0.0.1:8000/api/users/1/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["email"],
                         json.loads(self.new_user.content)["email"])
        self.assertEqual(json.loads(response.content)["id"],
                         json.loads(self.new_user.content)["id"])
        self.assertEqual(json.loads(response.content)["username"],
                         json.loads(self.new_user.content)["username"])
        self.assertEqual(json.loads(response.content)["first_name"],
                         json.loads(self.new_user.content)["first_name"])
        self.assertEqual(json.loads(response.content)["last_name"],
                         json.loads(self.new_user.content)["last_name"])
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
        self.assertEqual(json.loads(response.content)["email"],
                         json.loads(self.new_user.content)["email"])
        self.assertEqual(json.loads(response.content)["id"],
                         json.loads(self.new_user.content)["id"])
        self.assertEqual(json.loads(response.content)["username"],
                         json.loads(self.new_user.content)["username"])
        self.assertEqual(json.loads(response.content)["first_name"],
                         json.loads(self.new_user.content)["first_name"])
        self.assertEqual(json.loads(response.content)["last_name"],
                         json.loads(self.new_user.content)["last_name"])
        self.assertNotIn("password", json.loads(response.content))

    def test_user_reset_password(self):
        """
        Проверяем возможность смены пароля через api
        """
        self.client.post('http://127.0.0.1:8000/api/users/',
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
        self.assertTrue(check_password(data['new_password'],
                                       FoodUser.objects.get().password))


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


class TagsTests(APITestCase):

    def setUp(self):
        self.tag_info = {
            'name': 'test_tag',
            'color': 'test_color',
            'slug': 'test_slug'
        }

        Tag.objects.create(**self.tag_info)

    def test_tag_create_in_db(self):
        """
        Проверяем что тестовый тег создался в базе
        """
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().name, self.tag_info['name'])
        self.assertEqual(Tag.objects.get().color, self.tag_info['color'])
        self.assertEqual(Tag.objects.get().slug, self.tag_info['slug'])

    def test_tag_list(self):
        """
        Проверяем работоспособность списка тегов
        """
        url = 'http://127.0.0.1:8000/api/tags/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['id'], 1)
        self.assertEqual(json.loads(response.content)[0]['name'],
                         self.tag_info['name'])
        self.assertEqual(json.loads(response.content)[0]['color'],
                         self.tag_info['color'])
        self.assertEqual(json.loads(response.content)[0]['slug'],
                         self.tag_info['slug'])

    def test_tag_by_id(self):
        """
        Проверяем работоспособность получения тега по id
        """
        url = 'http://127.0.0.1:8000/api/tags/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['id'], 1)
        self.assertEqual(json.loads(response.content)['name'],
                         self.tag_info['name'])
        self.assertEqual(json.loads(response.content)['color'],
                         self.tag_info['color'])
        self.assertEqual(json.loads(response.content)['slug'],
                         self.tag_info['slug'])


class IngrediendsTests(APITestCase):
    def setUp(self):
        self.ingrediend_info = {
            'name': 'test_name',
            'measurement_unit': 'test_mu'
        }

        Ingredient.objects.create(**self.ingrediend_info)

    def test_ingredient_create_in_db(self):
        """
        Проверяем что тестовый ингредиент создался в базе
        """
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertEqual(Ingredient.objects.get().name,
                         self.ingrediend_info['name'])
        self.assertEqual(Ingredient.objects.get().measurement_unit,
                         self.ingrediend_info['measurement_unit'])

    def test_ingredient_list(self):
        """
        Проверяем работоспособность списка ингредиентов
        """
        url = 'http://127.0.0.1:8000/api/ingredients/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['id'], 1)
        self.assertEqual(json.loads(response.content)[0]['name'],
                         self.ingrediend_info['name'])
        self.assertEqual(json.loads(response.content)[0]['measurement_unit'],
                         self.ingrediend_info['measurement_unit'])

    def test_query_in_ingredient_list(self):
        """
        Проверяем работоспособность query-параметра name
        """
        url = 'http://127.0.0.1:8000/api/ingredients/?search=test'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['id'], 1)
        self.assertEqual(json.loads(response.content)[0]['name'],
                         self.ingrediend_info['name'])
        self.assertEqual(json.loads(response.content)[0]['measurement_unit'],
                         self.ingrediend_info['measurement_unit'])

        url = 'http://127.0.0.1:8000/api/ingredients/?search=fake'

        response = self.client.get(url, format='json')
        json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])

    def test_ingredient_by_id(self):
        """
        Проверяем работоспособность получения ингредиента по id
        """
        url = 'http://127.0.0.1:8000/api/ingredients/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['id'], 1)
        self.assertEqual(json.loads(response.content)['name'],
                         self.ingrediend_info['name'])
        self.assertEqual(json.loads(response.content)['measurement_unit'],
                         self.ingrediend_info['measurement_unit'])
