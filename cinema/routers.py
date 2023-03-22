from rest_framework.routers import DefaultRouter

from cinema_hall import views as cinema_hall_views

router = DefaultRouter()

router.register(
    "cinema",
    cinema_hall_views.CinemaModelViewSet,
    basename="cinema",
)
router.register(
    "hall",
    cinema_hall_views.HallModelViewSet,
    basename="hall",
)
router.register(
    "seat",
    cinema_hall_views.SeatModelViewSet,
    basename="seat",
)
