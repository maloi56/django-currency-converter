from http import HTTPStatus

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from rest_framework.test import APITestCase


class UsersApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = {'username': 'testuser',
                     'email': 'testuser@mail.ru',
                     'password': 'testtesttest1'}

        password = make_password(self.user['password'])
        self.created_user = User.objects.create(username='testtest', password=password)

        path = reverse('login')
        response = self.client.post(path,
                                    data={'username': self.created_user.username, 'password': self.user['password']},
                                    format='json')
        self.headers = {'Authorization': f'Token {response.data["auth_token"]}'}

    def test_registration_post(self):
        '''Тестирование успешной регистрации'''

        username = self.user['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        path = reverse('user-list')

        hard_pass = self.user['password']
        response = self.client.post(path, data={'username': username, 'password': hard_pass}, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_registration_post_error(self):
        '''Тестирование регистрации с ошибкой'''

        username = self.user['username']
        path = reverse('user-list')

        easy_pass = '123456'
        response = self.client.post(path, data={'username': username, 'password': easy_pass}, format='json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        User.objects.create(username=username, password=self.user['password'])
        response = self.client.post(path, self.user, format='json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_login_post(self):
        '''Тестирование авторизации'''

        password = make_password(self.user['password'])
        user = User.objects.create(username=self.user['username'], password=password)
        self.assertTrue(User.objects.filter(username=user.username).exists())

        path = reverse('login')
        response = self.client.post(path,
                                    data={'username': user.username, 'password': self.user['password']},
                                    format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_currency_post(self):
        '''Тестирование получение курсов валют'''

        path = reverse('api:currency')

        response = self.client.get(path, )  # без авторизации
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response = self.client.get(path, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), 44)

        path_with_query = path + '?valute=USD'
        response = self.client.get(path_with_query, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), 1)

        path_with_fault_query = path + '?valute=US'
        response = self.client.get(path_with_fault_query, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


    def test_convert_post(self):
        '''Тестирование конвертирования валют'''

        path = reverse('api:convert')

        response = self.client.get(path, )  # без авторизации
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        path_with_query = path + '?from=USD&to=RUB&amount=3'
        response = self.client.get(path_with_query, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), 1)

        path_with_fault_from = path + '?from=US&to=RUB&amount=3'
        response = self.client.get(path_with_fault_from, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        path_with_fault_to = path + '?from=USD&to=RU&amount=3'
        response = self.client.get(path_with_fault_to, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        path_with_fault_to = path + '?from=USD&to=RUB&amount=five'
        response = self.client.get(path_with_fault_to, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        path_with_lower_case = path + '?from=usd&to=rub&amount=3'
        response = self.client.get(path_with_lower_case, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)