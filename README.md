# Movie Ticket Booking - Backend (Django + DRF)

## Overview
Simple Movie Ticket Booking backend built with Django and Django REST Framework.
Features:
- Signup and Login (JWT via simplejwt)
- Movies, Shows, Bookings models
- Booking logic: prevents double booking and overbooking, cancelling frees seat
- Swagger API docs at `/swagger/`

## Setup (local)
1. Clone or copy this project into a folder.
2. Create and activate a virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
