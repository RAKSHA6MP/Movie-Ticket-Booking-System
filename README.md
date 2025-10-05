# Movie Ticket Booking - Backend (Django + DRF)

# Movie Ticket Booking System

A Django-based web application to manage movies, shows, and ticket bookings with JWT authentication and REST APIs.  

---

## **Features**

- Add, view, and manage Movies, Shows, and Bookings.  
- User authentication with JWT tokens.  
- Book seats for shows.  
- API endpoints documented in Swagger.  

---

## **Setup Instructions**

### **1. Clone the repository**
```bash
git clone https://github.com/RAKSHA6MP/Movie-Ticket-Booking-System.git
cd Movie-Ticket-Booking-System

1. Install dependencies
bash
pip install -r requirements.txt

2. Run migrations
bash
python manage.py makemigrations
python manage.py migrate

3. Create superuser (Admin)
bash
python manage.py createsuperuser
Follow the prompts to set username/email/password.

4. Run the development server
bash
python manage.py runserver
Open in browser: http://127.0.0.1:8000/admin/

Swagger API Documentation
Swagger UI provides full documentation of all available APIs:

http://127.0.0.1:8000/swagger/

You can interactively test:

GET /movies/ → List all movies

GET /movies/{id}/shows/ → List shows for a movie

POST /shows/{id}/book/ → Book seats for a show

JWT Authentication
Obtain JWT tokens (access & refresh) using the /api/token/ endpoint (if implemented).

Include token in request headers for protected endpoints:

makefile
Authorization: Bearer <access_token>

Project Structure
bash
movie_booking/
├─ booking/            # Django app for movies, shows, bookings
│  ├─ migrations/      # Database migrations
│  ├─ admin.py         # Register models for admin panel
│  ├─ models.py        # Movie, Show, Booking models
│  ├─ serializers.py   # DRF serializers
│  ├─ views.py         # API views
├─ movie_booking/       # Project settings
│  ├─ settings.py
│  ├─ urls.py
├─ manage.py            # Django management script
├─ requirements.txt
└─ README.md


Contributing
Feel free to fork the project, open issues, or submit pull requests.