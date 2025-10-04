# Skift i København (Copenhagen Transfer Guide)
Skift i København is a web application that helps users find the best carriage to board on Copenhagen's public transit for optimal transfers between lines and stations.

## Features
- Search for stations and lines in Copenhagen's public transit system (Metro, S-Tog)
- Get recommendations for the best carriage to board for easy transfers
- View and contribute transfer tips for each station

## Technology
- Django (Python web framework)
- Bootstrap for responsive UI

## Setup
This repository only contains the `skift-kbh` Django app. You must create a Django project and add the app to it. Please note that static files are not included in this repository.

### To set up the app:

1. **Create a new Django project** (if you don't already have one):
   ```sh
   django-admin startproject skift-kbh-project
   cd skift-kbh-project
   ```
2. **Clone this GitHub repository inside your Django project directory:**
3. **Add `'skift-kbh'` to `INSTALLED_APPS` in your `settings.py`.**
4. **Include the app's URLs in your main `urls.py`:**
   ```python
   from django.urls import path, include
   urlpatterns = [
       # ...
       path('', include('skift-kbh.urls')),
   ]
   ```
5. **Create a `static/` folder and add required static files (Bootstrap, CSS, etc.) as needed.**
6. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
7. **Create a superuser (optional, for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
8. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
9. **Access the app:**
    Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Contributing
Contributions and suggestions are welcome! Please open an issue or submit a pull request.

## Thanks
This project is based on the original ["Umsteigen in Berlin"](https://github.com/paulberlin/umsteigen) by Paul Führing, which provided transfer tips for Berlin's BVG. Many thanks to Paul Führing for the inspiration and groundwork.



