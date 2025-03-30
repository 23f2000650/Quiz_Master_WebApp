# Quiz Application

## Author
**Ashirwad**  
**Student ID:** 23F2000650  
**Email:** 23f2000650@ds.study.iitm.ac.in  

## About Me
I am passionate about coding and spend countless hours honing my programming skills. I enjoy the thrill of solving challenges and collaborating with other tech enthusiasts. Beyond coding, I am curious, analytical, and love to keep up with the latest tech trends and innovations.  

## Description
Our platform is an interactive hub for quizzes, offering seamless creation, participation, and performance tracking. Users can take quizzes to test their knowledge, while admins can organize and track quiz performance effortlessly.  

It provides in-depth analytics, helping users assess their knowledge while enabling admins to track engagement, accuracy, and trends. The system ensures interactive learning, engagement, and insightful analytics, benefiting both quiz takers and organizers.

---

## Technologies Used
- **Flask:** A lightweight backend framework for building web applications with Python.
- **SQLAlchemy:** ORM (Object-Relational Mapping) tool for database interactions.
- **SQLite:** Database management system for storing application data.
- **Vue.js:** A progressive JavaScript framework for building user interfaces and enhancing interactivity, complemented by CSS for styling.
- **Flask JWT Extended:** An extension that provides tools for managing user sessions and authentication using JSON Web Tokens (JWT).
- **Celery:** An asynchronous task queue that enables the execution of background jobs and scheduled tasks.
- **Redis:** An in-memory data structure store used as a caching database to optimize application performance.
- **ChartJS:** Used for creating interactive charts and visualizations on the admin + user dashboard.
- **Flask-Mail:** Used to send emails in Flask applications by integrating SMTP.

---

## Database Schema Design
The database schema is designed to effectively manage and organize the application's data by encompassing several key tables:
- **Users**
- **Subjects**
- **Chapters**
- **Quizzes**
- **Questions**
- **Quiz Results**

Relationships between these tables are established through foreign keys, allowing for seamless navigation and data integrity. For instance, the `quizzes` table links to `subjects` and `chapters`, while the `quiz_results` table connects to both `quiz` and `users` to track individual responses. This interconnected design enables efficient querying and reporting, facilitating the tracking of user activities and performance metrics within the system.

---

## API Design
I have created an API for managing a Quiz Web App, enabling users to interact with quizzes, questions, and results.
The API includes endpoints for:
- **User Management**
- **Retrieving Quizzes**
- **Fetching Quiz Details**
- **Storing Quiz Results**

It was implemented using Flask with Flask-RESTful, SQLAlchemy for database management, and JWT-based authentication for security.

A YAML file is provided for API Endpoints:
- **Main App**
- **Admin**
- **User**

---

## Architecture and Features
The project is organized into backend and frontend components, following a modular and scalable architecture.

### Backend Structure
The backend is structured with clear separation of concerns:
- **API Endpoints**
  - `backend/api/admin/` → Handles administrative functionalities (e.g., managing users, quizzes, reports).
  - `backend/api/user/` → Manages user-related operations (e.g., taking quizzes, fetching results).
- **Core Application Files**
  - `app.py` → Entry point for the Flask application.
  - `model.py` → Defines database models using Flask-SQLAlchemy.
  - `utils.py` → Contains helper functions for various utilities.
  - `.env` → Stores environment variables for secure configuration.
  - `requirements.txt` → Lists dependencies required for the project.
- **Task Scheduling & Background Jobs**
  - `celery_worker.py` → Configures Celery workers for handling asynchronous jobs.
  - `dump.rdb` → Redis database dump for caching.

### Frontend Structure
The frontend, built with Vue.js, follows a component-based architecture:
- **Components (`frontend/src/components/`)**
  - `admin/` → Contains Vue components for the admin dashboard and management panels.
  - `user/` → Includes UI components for quiz participation, results, and user interactions.
- **Assets (`frontend/src/assets/`)** → Holds static resources like images, styles, and icons.
- **Routing (`frontend/src/router/`)** → Manages client-side navigation using Vue Router.
- **Views (`frontend/src/views/`)** → Defines page-level components.
- **Main App Files**
  - `App.vue` → Root Vue component.
  - `main.js` → Initializes the Vue application.
  - `server.js` → Handles server-side rendering or API proxying if needed.

---

## Features
The project integrates essential and advanced functionalities:

### Default Features:
- **User Authentication:** Secure login and registration using Flask-JWT or Flask-Login.
- **Database Management:** Structured with Flask-SQLAlchemy and migrations handled via Flask-Migrate.
- **Admin Dashboard:** Allows administrators to manage quizzes, users, and reports.
- **Quiz System:** Users can take quizzes, view scores, and track progress.
- **RESTful APIs:** Separate API endpoints for admin and user operations.

### Additional Features:
- **Async Task Execution:** Celery and Redis handle background tasks like email notifications and data processing.
- **Automated Reports & Notifications:** Daily reminders and monthly reports sent via Google Chat Webhooks and email.
- **Data Export:** CSV and JSON export functionality for quiz results and analytics.
- **Optimized Performance:** Caching with Redis to reduce database queries and improve response times.
- **AI-Powered Automation:** LLM-based text processing and validation for offer letters and other documents.

---

## Video
Here’s a video link for the demo of the Quiz App: **[Click Here](#)**

## To run
- run vue.js using
- `npm run serve `
- run app.py
- `python app.py`
- run redis
- `redis-server`
- run celery
- `celery -A app.celery worker --loglevel=info`
- `celery -A app.celery beat --loglevel=info`
- To stop the redis server
- `sudo systemctl stop redis`
