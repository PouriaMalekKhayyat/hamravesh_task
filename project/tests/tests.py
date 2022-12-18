from rest_framework.test import APITestCase
from project.models import App
from rest_framework import status
from django.urls import reverse


class AppTestCase(APITestCase):
    def setUp(self):
        App.objects.create(name='testapp1', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp2', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp3', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp4', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp5', image='redis:latest', envs=None, command=None)

    def test_app_list(self):
        response = self.client.get(reverse('app_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_app_detail(self):
        response = self.client.get(reverse('app_detail', kwargs={'id': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_app_run(self):
        response = self.client.post(reverse('app_run', kwargs={'id': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RunTestCase(APITestCase):
    def setUp(self):
        App.objects.create(name='testapp1', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp2', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp3', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp4', image='redis:latest', envs=None, command=None)
        App.objects.create(name='testapp5', image='redis:latest', envs=None, command=None)

    def test_run_list(self):
        response = self.client.get(reverse('run_list', kwargs={'id': 4}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)