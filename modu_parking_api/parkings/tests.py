from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from parkings.models import Parking


class ParkingTestCase(APITestCase):
    def setUp(self) -> None:
        self.parking = baker.make(Parking, _quantity=3)

    def test_update(self):
        data = {
            'lot': '',
            'parking_time': 0.5,
        }햣 
        response = self.client.put(f'/api/parkings/{self.parkings[0].pk}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)