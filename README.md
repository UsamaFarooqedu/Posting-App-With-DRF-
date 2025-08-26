# Posting-App-With-DRF
In which I design the API with DRF to handle the CRUD operations 

Posting Web API with Django REST Framework
A RESTful API for a posting web application with user authentication and full CRUD operations.

Features
User Authentication: JWT-based authentication system

CRUD Operations: Create, read, update, and delete posts

User Management: User registration and profile management

Permissions: Role-based access control

RESTful API: Clean, standardized API endpoints

Tech Stack
Django 4.2+

Django REST Framework

Simple JWT for authentication

SQLite (can be configured for other databases)

CORS headers for cross-origin requests

API Endpoints
Authentication Endpoints
User registration

User login with JWT token obtainment

Token refresh functionality

Current user information retrieval

Posts Endpoints
List all posts (public access)

Create new posts (authenticated users only)

Retrieve specific posts

Update posts (owner-only access)

Delete posts (owner-only access)

Filter posts by user

Users Endpoints
List all users (admin access only)

Retrieve user profiles

Update user profiles (owner-only access)

Usage Examples
User Registration
Send a POST request with username, email, and password to the registration endpoint.

User Login
Authenticate with username and password to receive access and refresh tokens.

Post Management
Create, read, update, and delete posts using appropriate HTTP methods with authentication tokens.
