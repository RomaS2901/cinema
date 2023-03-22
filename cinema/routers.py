from rest_framework.routers import DefaultRouter

from cinema_hall import views as cinema_hall_views

router = DefaultRouter()

router.register(
    "cinema",
    cinema_hall_views.CinemaModelViewSet,
    basename="cinema",
)
