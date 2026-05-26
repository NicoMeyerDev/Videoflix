# 📦 Videoflix Backend

Videoflix is a containerized video streaming backend inspired by modern streaming platforms.

Built with Django 6, Django REST Framework, PostgreSQL, Redis and ffmpeg, the system handles user authentication, video uploads, asynchronous processing and automatic HLS conversion for adaptive streaming.

Uploaded videos are automatically converted into multiple resolutions (480p, 720p, 1080p) and prepared for playback in HLS-compatible players.

---

## 🚀 Features

✅ User registration with email activation  
✅ JWT authentication using HttpOnly cookies  
✅ Password reset via email  
✅ Secure login and session handling  
✅ Video upload through Django Admin  
✅ Automatic HLS conversion (480p / 720p / 1080p) using ffmpeg  
✅ Automatic thumbnail generation  
✅ Background processing with Redis + Django RQ  
✅ Dockerized environment for reproducible setup  
✅ PostgreSQL database integration  

---

## 🛠️ Tech Stack

- Python 3.12
- Django 6.0.4
- Django REST Framework
- PostgreSQL
- Redis
- Django RQ
- ffmpeg
- Docker & Docker Compose
- JWT Authentication

---

## 📋 Requirements

Install the following tools before starting:

- Docker
- Git

ℹ️ Django, PostgreSQL, Redis, ffmpeg and all dependencies are installed automatically inside Docker containers.

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/NicoMeyerDev/Videoflix
cd Videoflix
```

### 2. Create environment file

Windows:

```bash
copy .env.template .env
```

Mac/Linux:

```bash
cp .env.template .env
```

Open `.env` and insert your values:

```env
SECRET_KEY=your-secret-key

DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=your-password

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

DEFAULT_FROM_EMAIL=your@gmail.com
FRONTEND_URL=http://127.0.0.1:5500
```

For Gmail authentication an App Password is required.

---

### 3. Start containers

```bash
docker compose up --build -d
```

Start database migrations:

```bash
docker compose exec backend python manage.py migrate
```

Create admin account:

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## ▶️ Run application

Backend available at:

```text
http://localhost:8000/
```

Admin panel:

```text
http://localhost:8000/admin/
```

---

## 🎥 Video Processing Workflow

1. Upload video via Django Admin  
2. Background task starts automatically  
3. ffmpeg converts video to HLS format  
4. Resolutions generated (480p / 720p / 1080p)  
5. Thumbnail generated automatically  
6. Stream-ready output stored for playback 