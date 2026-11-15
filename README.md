# 🎵 Album Review App

A web application for discovering music albums and managing a personal album collection.

The application allows users to register and log in, search for albums using the Spotify API, add albums to their personal collection, and view album information.

## ✨ Features

- User registration and login
- Secure password hashing with bcrypt
- Album search using the Spotify Web API
- Album and artist information retrieved from Spotify
- Album cover images
- Personal album collection for each user
- Add albums to a personal collection
- Default `want to listen` status for newly added albums
- Album detail pages
- MySQL database with related tables
- Separate frontend and backend architecture
- REST API built with FastAPI
- Streamlit-based user interface

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **FastAPI**
- **MySQL**
- **SQL**
- **mysql-connector-python**
- **bcrypt**
- **Requests**
- **Pydantic**
- **Spotify Web API**
- **REST API**
- **JSON**
- **Markdown**

## 🔐 Authentication

The application uses a custom authentication system based on MySQL and bcrypt.

User passwords are never stored as plain text. Before being stored in the database, passwords are hashed using bcrypt.

During login, the entered password is verified against the stored hash.

The application stores the authenticated user's ID and username in Streamlit session state and uses the user ID to access user-specific data through the backend API.

## 🗄 Database

The application uses MySQL as its database.

The database contains five main tables:

- `users` — stores user accounts and password hashes
- `albums` — stores album information retrieved from Spotify
- `artists` — stores artist information
- `users_albums` — connects users with albums in their personal collections
- `reviews` — stores user reviews of albums

The `users_albums` table implements a many-to-many relationship between users and albums, allowing different users to maintain their own personal album collections.

## 🌐 REST API

The application uses FastAPI to provide a REST API between the Streamlit frontend and the MySQL database.

The frontend communicates with the backend through HTTP requests using the Requests library.

The backend handles application logic and database operations, while the frontend is responsible for displaying data and handling user interactions.

The application also integrates with the [Spotify Web API](https://developer.spotify.com/documentation/web-api) to retrieve album and artist information.

Spotify API requests are handled through a dedicated client.

## ## 📁 Project Structure

```text
album_review_app/
│
├── src/
│   └── album_review_app/
│       │
│       ├── backend/
│       │   ├── schemas/
│       │   │   ├── __init__.py
│       │   │   └── schemas.py
│       │   │
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── albums.py
│       │   │   ├── api_script.py
│       │   │   ├── artists.py
│       │   │   ├── router.py
│       │   │   └── users.py
│       │   │
│       │   ├── __init__.py
│       │   ├── api.py
│       │   └── db_request.py
│       │
│       ├── frontend/
│       │
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── home_page.py
│       │   ├── register.py
│       │   └── search_page.py
│       │
│       ├── __init__.py
│       ├── album_page.py
│       ├── app.log
│       ├── auth.py
│       ├── logger.py
│       ├── main.py
│       ├── spotify_api.py
│       └── ui.py
│
├── .env
├── .gitignore
├── app.log
├── pyproject.toml
├── README.md
└── uv.lock
```

### Main modules

**`backend/api.py`**

Creates the FastAPI application and registers API routers.

**`backend/db_request.py`**

Contains database connection logic and functions for executing MySQL queries.

**`backend/v1/router.py`**

Registers API routers and organizes API endpoints under the `/api/v1` prefix.

**`backend/v1/users.py`**

Contains API endpoints for user-related operations, including registration and user verification.

**`backend/v1/albums.py`**

Contains API endpoints for album-related operations, including retrieving user albums and managing personal collections.

**`backend/v1/artists.py`**

Contains API endpoints for artist-related operations.

**`backend/v1/api_script.py`**

Contains API-related functionality used by the backend.

**`backend/schemas/schemas.py`**

Contains Pydantic schemas for data validation and API request/response handling.

**`main.py`**

Entry point of the Streamlit application. Handles the login page and redirects authenticated users to the appropriate pages.

**`auth.py`**

Contains user registration and login logic, including password hashing and verification with bcrypt.

**`spotify_api.py`**

Handles communication with the Spotify Web API and retrieves album and artist information.

**`ui.py`**

Contains shared UI functionality, including sidebar navigation and authentication checks.

**`logger.py`**

Configures application logging.

**`pages/home_page.py`**

Displays the user's personal album collection.

**`pages/search_page.py`**

Provides album search functionality and allows users to add albums to their personal collection.

**`pages/register.py`**

Provides the user registration form.

**`album_page.py`**

Displays detailed information about a selected album.

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd album_review_app
```

### 2. Create a virtual environment

```bash
uv venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure MySQL

Create a MySQL database and configure the database connection for the application.

The database should contain the required `users`, `albums`, `artists`, `users_albums`, and `reviews` tables.

### 5. Configure environment variables

Create a `.env` file and add the required configuration:

```env
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

### 6. Run the backend

```bash
uv run uvicorn album_review_app.backend.api:app --reload
```

### 7. Run the frontend

```bash
uv run streamlit run src/album_review_app/frontend/main.py
```

The application will open in your browser.

## 📌 Future Improvements

- Add the ability to mark up to 3 or 5 albums as favorites
- Display favorite albums in a separate section on the home page
- Add the ability to open album details by clicking on album covers
- Implement album reviews
- Store and display user reviews
- Add more album collection management functionality
- Improve error handling and logging
- Improve API request caching and performance
- Deploy the application online

## 👩‍💻 About the Project

This project was created as a Python pet project to practice backend development, SQL, REST API design, authentication, external API integration, and frontend/backend architecture using Streamlit and FastAPI.