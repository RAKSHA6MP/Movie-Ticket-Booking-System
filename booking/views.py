from rest_framework import status, generics, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError, DatabaseError
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .models import Movie, Show, Booking
from .serializers import (
    SignupSerializer,
    MovieSerializer,
    ShowSerializer,
    BookingSerializer,
    CreateBookingSerializer,
)
import time

User = get_user_model()

# ------------------ Signup ------------------
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

# ------------------ Login ------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

@swagger_auto_schema(method="post", request_body=LoginSerializer)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials."}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })

# ------------------ List movies ------------------
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

# ------------------ Movie shows ------------------
class MovieShowsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        shows = movie.shows.all()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)

# ------------------ Book a seat ------------------
class BookSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CreateBookingSerializer,
        security=[{"Bearer": []}],
        responses={201: BookingSerializer}
    )
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seat_number = serializer.validated_data["seat_number"]

        if seat_number < 1 or seat_number > show.total_seats:
            return Response({"detail": f"seat_number must be between 1 and {show.total_seats}."},
                            status=status.HTTP_400_BAD_REQUEST)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                with transaction.atomic():
                    Show.objects.select_for_update().filter(pk=show.pk)

                    if Booking.objects.select_for_update().filter(show=show, seat_number=seat_number, status=Booking.STATUS_BOOKED).exists():
                        return Response({"detail": "Seat already booked."}, status=status.HTTP_400_BAD_REQUEST)

                    booked_count = Booking.objects.filter(show=show, status=Booking.STATUS_BOOKED).count()
                    if booked_count >= show.total_seats:
                        return Response({"detail": "Show is fully booked."}, status=status.HTTP_400_BAD_REQUEST)

                    booking = Booking.objects.create(
                        user=request.user,
                        show=show,
                        seat_number=seat_number,
                        status=Booking.STATUS_BOOKED,
                    )
                    out_serializer = BookingSerializer(booking)
                    return Response(out_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if "unique" in str(e).lower() or attempt + 1 == max_retries:
                    return Response({"detail": "Seat already booked (concurrent)."}, status=status.HTTP_400_BAD_REQUEST)
                time.sleep(0.1)
                continue
            except DatabaseError:
                if attempt + 1 == max_retries:
                    return Response({"detail": "Could not complete booking due to database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                time.sleep(0.1)
                continue

        return Response({"detail": "Could not complete booking."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ------------------ Cancel booking ------------------
class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(security=[{"Bearer": []}])
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if booking.user != request.user:
            return Response({"detail": "You cannot cancel someone else's booking."}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == Booking.STATUS_CANCELLED:
            return Response({"detail": "Booking is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            booking.status = Booking.STATUS_CANCELLED
            booking.save(update_fields=["status"])
        return Response({"detail": "Booking cancelled successfully."}, status=status.HTTP_200_OK)

# ------------------ My bookings ------------------
class MyBookingsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    @swagger_auto_schema(security=[{"Bearer": []}])
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")
