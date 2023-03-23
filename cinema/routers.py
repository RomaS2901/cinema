from rest_framework.routers import DefaultRouter

from cinema_hall import views as cinema_hall_views
from users import views as users_views

router = DefaultRouter()

router.register(
    "cinema",
    cinema_hall_views.CinemaViewSet,
    basename="cinema",
)
router.register(
    "hall",
    cinema_hall_views.HallViewSet,
    basename="hall",
)
router.register(
    "seat",
    cinema_hall_views.SeatViewSet,
    basename="seat",
)
router.register(
    "users",
    users_views.UserViewSet,
    basename="users",
)
