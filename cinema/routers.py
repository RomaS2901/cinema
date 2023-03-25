from django.urls import path
from rest_framework.routers import DefaultRouter

from cinema_hall import views as cinema_hall_views
from users import views as users_views
from screening import views as screening_views

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
    "movie",
    screening_views.MovieViewSet,
    basename="movie",
)
router.register(
    "screening_session",
    screening_views.ScreeningSessionViewSet,
    basename="screening_session",
)
router.register(
    "users",
    users_views.UserViewSet,
    basename="users",
)

urlpatterns = [
    path(
        "users/login/",
        users_views.login_api_view,
        name="login",
    ),
    path(
        "users/logout/",
        users_views.logout_api_view,
        name="logout",
    ),
]

urlpatterns += router.urls
