# PDF Chat Application

A web application that allows users to upload PDF documents, manage them, and chat with an AI assistant about the
contents of those PDFs using Gemini AI.

## Features

- **User Authentication**: Secure user registration and login system
- **PDF Management**: Upload, store, and manage PDF documents
- **PDF Processing**: Extract and index PDF content for chat functionality
- **AI Chat**: Interact with Gemini AI to ask questions about your PDF documents
- **MongoDB Integration**: Document storage using MongoDB database

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI Integration**: Google's Gemini AI
- **Authentication**: JWT-based authentication
- **PDF Processing**: Custom PDF parsing and storage services

## Project Structure

```
project-case/
├── app/
│   ├── libs/
│   │   ├── client.py
│   │   ├── hash.py
│   │   ├── exceptions/
│   │   │   └── pdf.py
│   │   └── services/
│   │       ├── chat.py
│   │       ├── gemini.py
│   │       └── pdf.py
│   ├── models/
│   │   ├── chat.py
│   │   └── user.py
│   ├── routers/
│   │   ├── chat.py
│   │   ├── pdf.py
│   │   └── user.py
│   └── schemas/
│       ├── chat.py
│       └── pdf.py
├── main.py
├── db.py
├── .env.example
└── README.md
```

## Setup and Installation

1. **Clone the repository**

```shell script
git clone https://github.com/mehmetkiran/project-case
   cd project-case
```

2. **Set up virtual environment**

```shell script
python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```shell script
pip install -r requirements.txt
```

4. **Environment configuration**
    - Copy `.env.example` to `.env`
    - Fill in the required environment variables:
        - MongoDB connection details
        - Gemini API key
        - JWT secret key

5.a **Run the application without Docker**

```shell script
uvicorn main:app --reload
```

5.b ** Run the application with Docker

To run the application using Docker Compose, make sure you have Docker and Docker Compose installed. Then, follow these
steps:

1. From the root directory of the project, start all services (FastAPI app, PostgreSQL, and MongoDB) with:

```shell script
   docker-compose up --build
```

2. This command will build the web service image and start all containers defined in the docker-compose.yml.
3. Once running, you can access the FastAPI application at:

```shell script
   http://localhost:8000
```

## API Endpoints

### Authentication

- `POST /users/register/` - Register a new user
- `POST /users/login/` - User login

### PDF Management

- `POST /pdf/pdf-upload/` - Upload a new PDF
- `GET /pdf/pdf-list` - Get list of user's PDFs
- `POST /pdf/pdf-parse/` - Parse a user's PDFs
- `POST /pdf/pdf-select/` - Select a user's PDFs

### Chat

- `GET /chat/chat-history` - Get list of chat sessions
- `POST /chat/pdf-chat` - Send a message in a chat

## How to Use It?

You can access and import the Postman collection from the following path:
```.postman/Project-Case.postman_collection.json```
Additionally, you can find example `curl` requests in the same directory:

## Known issues

* Base logger confing missing all logger function working properly.

## Limitations,

* There are no limitations identified at the moment.

## Improvement Ideas

* Logging confing
* Notification sent to the user when large files finish uploading