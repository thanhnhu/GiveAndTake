from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth.models import User
from .models.taker import Taker


class TakerCRUDTestCase(APITestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = APIClient()
        self.taker_url = '/api/takers/'

    def test_create_taker_success(self):
        # Prepare data
        taker_dict = {
            # 'user': User.objects.first(),
            'name': 'test_Pass',
        }

        # Make request
        # response = self.client.post(self.taker_url, taker_dict, format='json')
        # Check status response
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Taker.objects.count(), 2)
        # Check database
        # new_taker = Taker.objects.get(id=response.id)
        # self.assertEqual(
        #    new_taker.user,
        #    User.objects.first(),
        # )
        # self.assertEqual(
        #     new_taker.name,
        #     taker_dict.name,
        # )

    def test_get_takers_success(self):
        # Make request
        response = self.client.get(self.taker_url, format='json')
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert Taker.objects.count() == 0
