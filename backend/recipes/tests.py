import json

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Tag, Ingredient, Recipe
from users.models import FoodUser

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
        self.assertEqual(json.loads(response.content)[0]['name'], self.tag_info['name'])
        self.assertEqual(json.loads(response.content)[0]['color'], self.tag_info['color'])
        self.assertEqual(json.loads(response.content)[0]['slug'], self.tag_info['slug'])

    def test_tag_by_id(self):
        """
        Проверяем работоспособность получения тега по id
        """
        url = 'http://127.0.0.1:8000/api/tags/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['id'], 1)
        self.assertEqual(json.loads(response.content)['name'], self.tag_info['name'])
        self.assertEqual(json.loads(response.content)['color'], self.tag_info['color'])
        self.assertEqual(json.loads(response.content)['slug'], self.tag_info['slug'])

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
        self.assertEqual(Ingredient.objects.get().name, self.ingrediend_info['name'])
        self.assertEqual(Ingredient.objects.get().measurement_unit, self.ingrediend_info['measurement_unit'])

    def test_ingredient_list(self):
        """
        Проверяем работоспособность списка ингредиентов
        """
        url = 'http://127.0.0.1:8000/api/ingredients/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['id'], 1)
        self.assertEqual(json.loads(response.content)[0]['name'], self.ingrediend_info['name'])
        self.assertEqual(json.loads(response.content)[0]['measurement_unit'], self.ingrediend_info['measurement_unit'])

    def test_query_in_ingredient_list(self):
        """
        Проверяем работоспособность query-параметра name
        """
        url = 'http://127.0.0.1:8000/api/ingredients/?search=test'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['id'], 1)
        self.assertEqual(json.loads(response.content)[0]['name'], self.ingrediend_info['name'])
        self.assertEqual(json.loads(response.content)[0]['measurement_unit'], self.ingrediend_info['measurement_unit'])

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
        self.assertEqual(json.loads(response.content)['name'], self.ingrediend_info['name'])
        self.assertEqual(json.loads(response.content)['measurement_unit'], self.ingrediend_info['measurement_unit'])

class RecipesTests(APITestCase):
    def setUp(self):
        self.ingrediend_info1 = {
            'name': 'test_name1',
            'measurement_unit': 'test_mu1'
        }
        self.ingrediend_info2 = {
            'name': 'test_name2',
            'measurement_unit': 'test_mu2'
        }
        new_ing1 = Ingredient.objects.create(**self.ingrediend_info1)
        new_ing2 = Ingredient.objects.create(**self.ingrediend_info2)

        self.tag_info1 = {
            'name': 'test_tag1',
            'color': 'test_color1',
            'slug': 'test_slug1'
        }
        self.tag_info2 = {
            'name': 'test_tag2',
            'color': 'test_color2',
            'slug': 'test_slug2'
        }
        new_tag1 = Tag.objects.create(**self.tag_info1)
        new_tag2 = Tag.objects.create(**self.tag_info2)

        self.user_info = {
            'email': 'test@test.com',
            'username': 'testname',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'testpassword123!'
        }
        new_user = FoodUser.objects.create_user(**self.user_info)

        self.recipe_info = {
            "ingredients": [
                {
                "id": 1,
                "amount": 10
                }
            ],
            "tags": [
                1,
                2
            ],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
            }

        Recipe.objects.create(**self.recipe_info)
    
    def test_recipe_create_in_db(self):
        """
        Проверяем что тестовый рецепт создался в базе
        """
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().name, self.recipe_info['name'])
        self.assertEqual(Recipe.objects.get().image, self.recipe_info['image'])
        self.assertEqual(Recipe.objects.get().author, self.recipe_info['author'])
        self.assertEqual(Recipe.objects.get().ingredients, self.recipe_info['ingredients'])
        self.assertEqual(Recipe.objects.get().tags, self.recipe_info['tags'])
