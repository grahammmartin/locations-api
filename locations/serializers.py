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

