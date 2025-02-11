# Django API Authentication and Profile Management

## Overview

This project is a Django-based authentication and profile management system with API endpoints. It includes functionalities such as:

- User registration with email verification
- User login with token authentication
- Profile management for users and viewers
- Password reset functionality

## Features

- **Authentication & Authorization**: User login, registration, and authentication with Django Rest Framework (DRF) and token-based authentication.
- **Email Verification**: Users must confirm their email address before activating their account.
- **Profile Management**: Users can update their profiles, including usernames and email addresses.
- **Password Reset**: Users can reset their password via email verification.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repository-url.git
cd your-project-directory
```

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add the following variables:

```plaintext
# Email Backend Settings
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.example.com  # Replace with your email provider
EMAIL_HOST_USER = your-email@example.com  # Replace with your email address
EMAIL_HOST_PASSWORD = your-email-password  # Replace with your email password or app password
EMAIL_PORT = 587  # Default SMTP port (may vary)
EMAIL_USE_TLS = True  # Set to True for TLS encryption
EMAIL_USE_SSL = False  # Set to True if your provider requires SSL

#Domain
DOMAIN_REDIRECT = http://localhost:4200  # Replace with your frontend domain
ROOT_DOMAIN = http://127.0.0.1:8000  # Replace with your backend domain
```

Ensure the `.env` file is included in `.gitignore` to prevent exposing credentials.

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint                                                       | Description                                |
| ------ | -------------------------------------------------------------- | ------------------------------------------ |
| POST   | `/api/authentication/register/`                                | Register a new user                        |
| GET    | `/api/authentication/activate/<uidb64>/<token>/`               | Activate user account                      |
| POST   | `/api/login/`                                                  | User login and obtain authentication token |
| POST   | `/api/authentication/password-reset/`                          | Request password reset                     |
| GET    | `/api/authentication/password-reset-confirm/<uidb64>/<token>/` | Confirm password reset                     |

### Profile Endpoints

| Method | Endpoint                 | Description                      |
| ------ | ------------------------ | -------------------------------- |
| GET    | `/api/profile/<int:pk>/` | Get user profile by ID           |
| PATCH  | `/api/profile/<int:pk>/` | Update user profile              |
| GET    | `/api/viewer/`           | Get viewer profiles              |
| POST   | `/api/viewer/`           | Create a new viewer profile      |
| GET    | `/api/viewer/<int:pk>/`  | Retrieve a single viewer profile |
| PATCH  | `/api/viewer/<int:pk>/`  | Update viewer profile            |
| DELETE | `/api/viewer/<int:pk>/`  | Delete viewer profile            |

## Project Structure

```
project_directory/
├── env/                # Virtual environment
├── manage.py           # Django entry point
├── requirements.txt    # Dependencies
├── .env                # Environment variables (not in repository)
├── README.md           # Documentation
├── authentication/     # Authentication app
├── profile_user_app/   # User profile management app
├── profile_viewer_app/ # Viewer profile management app
├── content_app/        # Video content app
```

## Dependencies

The required dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

To update dependencies:

```bash
pip freeze > requirements.txt
```

## Notes

- Ensure the virtual environment is activated before running the project.
- Never commit sensitive data such as passwords or API keys to the repository.
- Always test API endpoints using tools like Postman or Django's built-in API browser.
