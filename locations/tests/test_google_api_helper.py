import unittest
from unittest.mock import Mock, patch

from django.conf import settings

from ..helpers import GoogleAPIHelper


class GoogleAPIHelperTest(unittest.TestCase):
    def setUp(self):
        self.api_key = "fake_api_key"
        settings.GOOGLE_MAPS_API_KEY = self.api_key
        self.helper = GoogleAPIHelper()
        self.valid_address = "1600 Amphitheatre Parkway, Mountain View, CA"
        self.valid_latitude = 37.4224764
        self.valid_longitude = -122.0842499

    @patch("requests.get")
    def test_get_by_address_success(self, mock_get):
        mock_response = Mock()
        expected_data = {
            "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            "latitude": self.valid_latitude,
            "longitude": self.valid_longitude
        }
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{
                "formatted_address": expected_data["formatted_address"],
                "geometry": {
                    "location": {
                        "lat": expected_data["latitude"],
                        "lng": expected_data["longitude"]
                    }
                }
            }]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.helper.get_by_address(self.valid_address)
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(self.helper.base_url, params={
            "address": self.valid_address,
            "key": self.api_key
        })

    @patch("requests.get")
    def test_get_by_address_failure(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ZERO_RESULTS"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.helper.get_by_address(self.valid_address)
        self.assertIsNone(result)
        mock_get.assert_called_once_with(self.helper.base_url, params={
            "address": self.valid_address,
            "key": self.api_key
        })

    @patch("requests.get")
    def test_get_by_coors_success(self, mock_get):
        mock_response = Mock()
        expected_data = {
            "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            "latitude": self.valid_latitude,
            "longitude": self.valid_longitude
        }
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{
                "formatted_address": expected_data["formatted_address"],
                "geometry": {
                    "location": {
                        "lat": expected_data["latitude"],
                        "lng": expected_data["longitude"]
                    }
                }
            }]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.helper.get_by_coors(self.valid_latitude, self.valid_longitude)
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(self.helper.base_url, params={
            "latlng": f"{self.valid_latitude},{self.valid_longitude}",
            "key": self.api_key
        })

    @patch("requests.get")
    def test_get_by_coors_failure(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ZERO_RESULTS"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.helper.get_by_coors(self.valid_latitude, self.valid_longitude)
        self.assertIsNone(result)
        mock_get.assert_called_once_with(self.helper.base_url, params={
            "latlng": f"{self.valid_latitude},{self.valid_longitude}",
            "key": self.api_key
        })

if __name__ == "__main__":
    unittest.main()
