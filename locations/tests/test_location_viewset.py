from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..helpers import GoogleAPIHelper


class LocationViewSetTest(APITestCase):

    @patch.object(GoogleAPIHelper, "get_by_address")
    def test_get_geocode_success(self, mock_get_by_address):
        mock_get_by_address.return_value = {
            "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            "latitude": 37.422476,
            "longitude": -122.084249
        }

        url = reverse("locations-get-geocode")
        data = {"user_address": "1600 Amphitheatre Parkway, Mountain View, CA"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["address"], data["user_address"])
        self.assertEqual(response.data["formatted_address"], mock_get_by_address.return_value["formatted_address"])
        self.assertEqual(response.data["latitude"], str(mock_get_by_address.return_value["latitude"]))
        self.assertEqual(response.data["longitude"], str(mock_get_by_address.return_value["longitude"]))

    @patch.object(GoogleAPIHelper, "get_by_address")
    def test_get_geocode_failure(self, mock_get_by_address):
        mock_get_by_address.return_value = None

        url = reverse("locations-get-geocode")
        data = {"user_address": "Invalid Address"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Results not found for Invalid Address", str(response.data))

    @patch.object(GoogleAPIHelper, "get_by_coors")
    def test_reverse_geocode_success(self, mock_get_by_coors):
        mock_get_by_coors.return_value = {
            "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            "latitude": 37.422476,
            "longitude": -122.084249
        }

        url = reverse("locations-reverse-geocode")
        data = {"latitude_input": 37.422476, "longitude_input": -122.084249}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["latitude"], str(data["latitude_input"]))
        self.assertEqual(response.data["longitude"], str(data["longitude_input"]))
        self.assertEqual(response.data["formatted_address"], mock_get_by_coors.return_value["formatted_address"])

    @patch.object(GoogleAPIHelper, "get_by_coors")
    def test_reverse_geocode_failure(self, mock_get_by_coors):
        mock_get_by_coors.return_value = None

        url = reverse("locations-reverse-geocode")
        data = {"latitude_input": 0.0, "longitude_input": 0.0}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(f"Results not found for {data['latitude_input']}, {data['longitude_input']}", str(response.data))

    @patch.object(GoogleAPIHelper, "get_by_address")
    @patch.object(GoogleAPIHelper, "get_by_coors")
    def test_calculate_distance(self, mock_get_by_address, mock_get_by_coors):
        mock_get_by_address.return_value = {
            "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            "latitude": 37.422476,
            "longitude": -122.084249
        }
        mock_get_by_coors.return_value = {
            "formatted_address": "1 Infinite Loop, Cupertino, CA 95014, USA",
            "latitude": 37.331820,
            "longitude": -122.031180
        }

        url = reverse("locations-calculate-distance")
        data = {
            "from_address": "1600 Amphitheatre Parkway, Mountain View, CA",
            "to_address": "1 Infinite Loop, Cupertino, CA"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("distance", response.data)
