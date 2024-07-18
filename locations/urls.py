from rest_framework.routers import DefaultRouter

from .views import LocationViewSet

router = DefaultRouter()

router.register("locations", LocationViewSet, "locations")

urlpatterns = router.urls
