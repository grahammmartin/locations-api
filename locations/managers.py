from django.db.models import Manager

from .helpers import GoogleAPIHelper


class LocationRequestManager(Manager):
    def __init__(self, *args, **kwargs):
        self.google_api = GoogleAPIHelper()

        super().__init__(*args, **kwargs)

    def get_or_create_by_address(self, address):
        try:
            return self.get(address=address)
        except self.model.DoesNotExist:
            data = self.google_api.get_by_address(address)

            if data is None:
                return self.create(address=address)

            return self.create(
                address=address,
                latitude=data["latitude"],
                longitude=data["longitude"],
                formatted_address=data["formatted_address"]
            )

    def get_or_create_by_coordinates(self, latitude, longitude):
        try:
            return self.get(latitude=latitude, longitude=longitude)
        except self.model.DoesNotExist:
            data = self.google_api.get_by_coors(latitude, longitude)

            if data is None:
                return self.create(latitude=latitude, longitude=longitude)

            return self.create(
                address=data["formatted_address"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                formatted_address=data["formatted_address"]
            )
        except self.model.MultipleObjectsReturned:
            return self.filter(latitude=latitude, longitude=longitude).first()
