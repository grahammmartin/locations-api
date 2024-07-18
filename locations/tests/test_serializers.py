import unittest
from unittest.mock import patch

from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from ..models import LocationRequest
from ..serializers import AddressLocationRequestSerializer, CoorsLocationRequestSerializer, DistanceLocationRequestSerializer


class AddressLocationRequestSerializerTest(APITestCase):

    @patch("locations.models.LocationRequest.maps.get_or_create_by_address")
    def test_create_success(self, mock_get_or_create_by_address):
        mock_get_or_create_by_address.return_value = LocationRequest(
            address="1600 Amphitheatre Parkway, Mountain View, CA",
            formatted_address="1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            latitude=37.422476,
            longitude=-122.084249
        )
        data = {"user_address": "1600 Amphitheatre Parkway, Mountain View, CA"}
        serializer = AddressLocationRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        location = serializer.save()
        self.assertEqual(location.address, data["user_address"])

    @patch("locations.models.LocationRequest.maps.get_or_create_by_address")
    def test_create_failure(self, mock_get_or_create_by_address):
        mock_get_or_create_by_address.return_value = LocationRequest(
            address="1600 Amphitheatre Parkway, Mountain View, CA",
            formatted_address="",
            latitude=37.422476,
            longitude=-122.084249
        )
        data = {"user_address": "1600 Amphitheatre Parkway, Mountain View, CA"}
        serializer = AddressLocationRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError) as context:
            serializer.save()
        self.assertIn("Results not found for", str(context.exception))

class CoorsLocationRequestSerializerTest(APITestCase):

    def test_valid_latitude_longitude(self):
        data = {"latitude_input": 37.422476, "longitude_input": -122.084249}
        serializer = CoorsLocationRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_latitude(self):
        data = {"latitude_input": 100.0, "longitude_input": -122.084249}
        serializer = CoorsLocationRequestSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Latitude must be between -90 and 90 degrees.", str(context.exception))

    def test_invalid_longitude(self):
        data = {"latitude_input": 37.422476, "longitude_input": 200.0}
        serializer = CoorsLocationRequestSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Longitude must be between -180 and 180 degrees.", str(context.exception))

    @patch("locations.models.LocationRequest.maps.get_or_create_by_coordinates")
    def test_create_success(self, mock_get_or_create_by_coordinates):
        mock_get_or_create_by_coordinates.return_value = LocationRequest(
            address="1600 Amphitheatre Parkway, Mountain View, CA",
            formatted_address="1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            latitude=37.422476,
            longitude=-122.084249
        )
        data = {"latitude_input": 37.422476, "longitude_input": -122.084249}
        serializer = CoorsLocationRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        location = serializer.save()
        self.assertEqual(location.latitude, data["latitude_input"])
        self.assertEqual(location.longitude, data["longitude_input"])

    @patch("locations.models.LocationRequest.maps.get_or_create_by_coordinates")
    def test_create_failure(self, mock_get_or_create_by_coordinates):
        mock_get_or_create_by_coordinates.return_value = LocationRequest(
            address="1600 Amphitheatre Parkway, Mountain View, CA",
            formatted_address="",
            latitude=37.422476,
            longitude=-122.084249
        )
        data = {"latitude_input": 37.422476, "longitude_input": -122.084249}
        serializer = CoorsLocationRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError) as context:
            serializer.save()
        self.assertIn("Results not found for", str(context.exception))

class DistanceLocationRequestSerializerTest(APITestCase):

    @patch("locations.helpers.haversine")
    @patch("locations.serializers.AddressLocationRequestSerializer.save")
    def test_create_success(self, mock_save, mock_haversine):
        mock_haversine.return_value = 10
        mock_save.side_effect = [
            LocationRequest(
                address="1600 Amphitheatre Parkway, Mountain View, CA",
                formatted_address="1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
                latitude=37.422476,
                longitude=-122.084249
            ),
            LocationRequest(
                address="1 Infinite Loop, Cupertino, CA",
                formatted_address="1 Infinite Loop, Cupertino, CA 95014, USA",
                latitude=37.331820,
                longitude=-122.031180
            )
        ]
        data = {
            "from_address": "1600 Amphitheatre Parkway, Mountain View, CA",
            "to_address": "1 Infinite Loop, Cupertino, CA"
        }
        serializer = DistanceLocationRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        result = serializer.save()
        self.assertEqual(result["from_address"], "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA")
        self.assertEqual(result["to_address"], "1 Infinite Loop, Cupertino, CA 95014, USA")
        self.assertEqual(result["distance"], "11.12 KM")

if __name__ == "__main__":
    unittest.main()
