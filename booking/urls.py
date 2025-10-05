from django.urls import path
from .views import (
    SignupView, login_view, MovieListView, MovieShowsView,
    BookSeatView, CancelBookingView, MyBookingsView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", login_view, name="login"),  # returns JWT tokens
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),

    path("movies/", MovieListView.as_view(), name="movies-list"),
    path("movies/<int:pk>/shows/", MovieShowsView.as_view(), name="movie-shows"),
    path("shows/<int:pk>/book/", BookSeatView.as_view(), name="book-seat"),
    path("bookings/<int:pk>/cancel/", CancelBookingView.as_view(), name="cancel-booking"),
    path("my-bookings/", MyBookingsView.as_view(), name="my-bookings"),
]
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Movie Booking API is running! Visit /swagger/ for docs."})

urlpatterns = [
    path("", home, name="home"),  # 👈 add this line
    path("signup", SignupView.as_view(), name="signup"),
    path("login", login_view, name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("movies/", MovieListView.as_view(), name="movies-list"),
    path("movies/<int:pk>/shows/", MovieShowsView.as_view(), name="movie-shows"),
    path("shows/<int:pk>/book/", BookSeatView.as_view(), name="book-seat"),
    path("bookings/<int:pk>/cancel/", CancelBookingView.as_view(), name="cancel-booking"),
    path("my-bookings/", MyBookingsView.as_view(), name="my-bookings"),
]



