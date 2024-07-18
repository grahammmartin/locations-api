import requests
from django.conf import settings


class GoogleAPIHelper:
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_by_address(self, address):
        params = {"address": address, "key": self.api_key}
        return self._fetch_location(params)

    def get_by_coors(self, latitude, longitude):
        params = {"latlng": f"{latitude},{longitude}", "key": self.api_key}
        return self._fetch_location(params)

    def _fetch_location(self, params):
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200 and response.json().get("status") == "OK":
            result = response.json()["results"][0]
            data = {
                "formatted_address": result["formatted_address"],
                "latitude": result["geometry"]["location"]["lat"],
                "longitude": result["geometry"]["location"]["lng"]
            }
            return data
        return None


