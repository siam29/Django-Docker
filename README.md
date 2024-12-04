# Inventory Management System
An efficient and scalable inventory management system built with Django. It supports features like property management, user authentication, and geospatial data integration.



## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Set up this project](#installation)
   - [Clone the repository](#clone-the-repository)
   - [Install dependencies](#install-dependencies)
   - [Set up environment variables](#set-up-environment-variables)
   - [Database setup](#database-setup)
5. [Running the Project](#running-the-project)
   - [Run Server](#run-server)
   - [Run Tests](#run-tests)

7. [Contributing](#contributing)
8. [License](#license)

---


## Project Overview
This project is designed to streamline the management of properties, users, and locations with features such as geospatial data integration, advanced user permissions, and import/export capabilities for data. Built with Django, it supports efficient workflows for property owners and admins.

## Features
- User Authentication and Role Management
- Geospatial Data Handling (Django GIS)
- Import/Export Data via Admin Panel
- Amenity Validation for JSON Fields
- Unit and Integration Testing with Pytest

## Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL with PostGIS
- **Testing**: `pytest`, `pytest-django`, `pytest-cov`
- **Geospatial**: Leaflet
- **Containerization**: Docker

## Set up this project
1. Clone the repository from GitHub

```
https://github.com/siam29/Django-Docker.git
```
2. Navigate to the inventory-management directory
```
cd inventory-management/
```
3. Create a Python virtual environment
```
python3 -m venv env
```
4. Activate the virtual environment
```
source env/bin/activate
```
5. Install required dependencies

```
pip install -r requirements.txt
```
6. Build the Docker container
```
docker-compose build
```
7. Up the Docker container
```
docker-compose up
```

8.Check the container
```
docker ps
```
9. Create superuser
```
docker exec -it inventoryManagement bash
python manage.py createsuperuser
```
Then show this messege. Fill up this carefully and remember the password 

- Username (leave blank to use 'root'): <Enter user name>
- Email address: 
- Password: 
- Password (again): 
- The password is too similar to the username.
- This password is too common.
- Bypass password validation and create user anyway? [y/N]: y
- Superuser created successfully.

After completing these steps, you will have a superuser created for your Django application. You can log into the Django admin panel by going to:

8. Make Migrations
```
docker exec -it inventoryManagement python manage.py makemigrations
```
9. Apply Migrations
```
docker exec -it inventoryManagement python manage.py migrate
```

10. Check the Status of Migrations
```
docker exec -it inventoryManagement python manage.py showmigrations
```

## Run this project
Go to the url and paste this command for registration a user
```
http://localhost:8000/signup/
```
Paste this url for the admin before create the superuser username and password now enter this for sign in admin.
```
http://localhost:8000/admin/
```
Admin can have ```Active``` ```Staff status``` and ```Superuser status``` options and provide it any user so that it can now login and add ```Accommodations```.
### Test this project
To run tests with coverage, use ```pytest```
```
docker exec -it inventoryManagement pytest --cov=properties --cov-report=term-missing
```
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any bug fixes or feature requests.

