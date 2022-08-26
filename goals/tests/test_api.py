from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from goals.models import Board
from goals.serializers import BoardListSerializer


class BoardApiTestCase(APITestCase):
    def test_get(self):
        board_1 = Board.objects.create(title='Test title 1')
        board_2 = Board.objects.create(title='Test title 2')
        url = reverse('board-list')
        response = self.client.get(url)
        serializer_data = BoardListSerializer([board_1, board_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
