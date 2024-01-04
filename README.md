# Status/Features
- [x] API endpoint
- [x] JWT Authentication for user
- [x] Rate limit and Throttling
- [x] Readme with setup instruction
- [ ] Tests

# Project Overview
This project aims to build a secure and scalable RESTful API for managing notes. Users can perform CRUD operations on their notes, share notes with other users, and search for notes based on keywords. The application focuses on security, scalability, and efficient search functionality.

## Technical Requirements
- **Framework:** Implemented using Flask, a micro web framework for Python, known for its simplicity and flexibility.
- **Database:** MongoDB is chosen as the database becasue of flexible schema design.
- **Authentication:** Implemented using JWT (JSON Web Tokens) for secure user authentication. Easily available with flask framework
- **Rate Limiting and Throttling:** Implemented using Flask-Limiter and gunicorn to control and limit the rate of incoming requests.
- **Search Functionality:** Utilizes text indexing in mongo for high-performance search functionality, enhancing the efficiency of note searches.

## API Endpoints

### Authentication Endpoints

- **POST /api/auth/signup:** Create a new user account.
- **POST /api/auth/login:** Log in to an existing user account and receive an access token.

### Note Endpoints

- **GET /api/notes:** Get a list of all notes for the authenticated user.
- **GET /api/notes/:id:** Get a note by ID for the authenticated user.
- **POST /api/notes:** Create a new note for the authenticated user.
- **PUT /api/notes/:id:** Update an existing note by ID for the authenticated user.
- **DELETE /api/notes/:id:** Delete a note by ID for the authenticated user.
- **POST /api/notes/:id/share:** Share a note with another user for the authenticated user.
- **GET /api/search?q=:query:** Search for notes based on keywords for the authenticated user.

## Setup
 - Clone Repository
    ```
    git clone git@github.com:harshit105/notes-sharing.git
    cd notes-sharing
    ```
 - Build and run docker image
    ```
    docker build --no-cache -t shared-notes .
    docker-compose up
    ```
 - Download resource/notes-sharing.postmal_collection.json file for api documentation
