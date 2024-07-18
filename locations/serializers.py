from rest_framework import serializers
from .models import LocationRequest


class BaseLocationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationRequest
        fields = "__all__"
        read_only_fields = ["id", "address", "latitude", "longitude", "formatted_address"]


class AddressLocationRequestSerializer(BaseLocationRequestSerializer):
    user_address = serializers.CharField(write_only=True)

    def create(self, validated_data):
        address = validated_data.pop("user_address")

        location = LocationRequest.maps.get_or_create_by_address(address)

        if not location.formatted_address:
            raise serializers.ValidationError(f"Results not found for {address}")

        return location


class CoorsLocationRequestSerializer(BaseLocationRequestSerializer):
    latitude_input = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    longitude_input = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)

    def validate_latitude_input(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
        return value

    def validate_longitude_input(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
        return value

    def create(self, validated_data):
        latitude = validated_data.pop("latitude_input")
        longitude = validated_data.pop("longitude_input")

        location = LocationRequest.maps.get_or_create_by_coordinates(latitude, longitude)

        if not location.formatted_address:
            raise serializers.ValidationError("Results not found for %.1f, %.1f" %(latitude, longitude))

        return location

