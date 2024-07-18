from unittest.mock import patch

from django.test import TestCase

from ..helpers import GoogleAPIHelper
from ..models import LocationRequest


class LocationRequestModelTest(TestCase):

    @patch.object(GoogleAPIHelper, "get_by_address")
    def test_get_or_create_by_address_existing(self, mock_get_by_address):
        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        formatted_address = "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA"
        latitude = 37.4224764
        longitude = -122.0842499

        location = LocationRequest.objects.create(
            address=address,
            formatted_address=formatted_address,
            latitude=latitude,
            longitude=longitude
        )

        mock_get_by_address.return_value = None

        retrieved_location = LocationRequest.maps.get_or_create_by_address(address)

        self.assertEqual(retrieved_location, location)
        mock_get_by_address.assert_not_called()

    @patch.object(GoogleAPIHelper, "get_by_address")
    def test_get_or_create_by_address_new(self, mock_get_by_address):
        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        formatted_address = "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA"
        latitude = 37.4224764
        longitude = -122.0842499
        mock_get_by_address.return_value = {
            "formatted_address": formatted_address,
            "latitude": latitude,
            "longitude": longitude
        }
        retrieved_location = LocationRequest.maps.get_or_create_by_address(address)

        self.assertEqual(retrieved_location.address, address)
        self.assertEqual(retrieved_location.formatted_address, formatted_address)
        self.assertEqual(retrieved_location.latitude, latitude)
        self.assertEqual(retrieved_location.longitude, longitude)
        mock_get_by_address.assert_called_once_with(address)

    @patch.object(GoogleAPIHelper, "get_by_coors")
    def test_get_or_create_by_coordinates_existing(self, mock_get_by_coors):
        latitude = 37.422476
        longitude = -122.084249
        address = "1600 Amphitheatre Parkway, Mountain View, CA"
        formatted_address = "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA"

        location = LocationRequest.objects.create(
            address=address,
            formatted_address=formatted_address,
            latitude=latitude,
            longitude=longitude
        )
        mock_get_by_coors.return_value = None
        retrieved_location = LocationRequest.maps.get_or_create_by_coordinates(latitude, longitude)

        self.assertEqual(retrieved_location, location)
        mock_get_by_coors.assert_not_called()

    @patch.object(GoogleAPIHelper, "get_by_coors")
    def test_get_or_create_by_coordinates_new(self, mock_get_by_coors):
        latitude = 37.4224764
        longitude = -122.0842499
        formatted_address = "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA"
        mock_get_by_coors.return_value = {
            "formatted_address": formatted_address,
            "latitude": latitude,
            "longitude": longitude
        }

        retrieved_location = LocationRequest.maps.get_or_create_by_coordinates(latitude, longitude)

        self.assertEqual(retrieved_location.address, formatted_address)
        self.assertEqual(retrieved_location.formatted_address, formatted_address)
        self.assertEqual(retrieved_location.latitude, latitude)
        self.assertEqual(retrieved_location.longitude, longitude)
        mock_get_by_coors.assert_called_once_with(latitude, longitude)
