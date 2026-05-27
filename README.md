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
- Django 6
- Django REST Framework
- PostgreSQL
- Redis
- Django RQ
- ffmpeg
- Docker & Docker Compose
- JWT Authentication

---

## 📋 Requirements

Install before starting:

- Docker
- Git

ℹ️ Django, PostgreSQL, Redis, ffmpeg and all required dependencies are installed automatically inside Docker containers.

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/NicoMeyerDev/Videoflix
cd Videoflix
```

---

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

ℹ️ Gmail requires an **App Password**, not your normal Gmail password.

---

### 3. Start containers

```bash
docker compose up --build -d
```

The entrypoint automatically:

- waits for PostgreSQL
- applies database migrations
- collects static files
- creates the default superuser (if not existing)

Default admin account:

```text
Username: admin
Password: adminpassword
Email: admin@example.com
```

---

## ▶️ Run application

Backend:

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

---

## ⚠️ Windows users: EntryPoint issue

If the backend container does not start and you see:

```text
exec ./backend.entrypoint.sh: no such file or directory
```

the file may use Windows line endings (`CRLF`) instead of Linux line endings (`LF`).

Fix in VS Code:

1. Open:

```text
backend.entrypoint.sh
```

2. Click `CRLF` (bottom right in VS Code)

3. Change to:

```text
LF
```

4. Save file

5. Rebuild containers:

```bash
docker compose down
docker compose up --build -d
```

---

## 🔐 Authentication Flow

Registration requires email activation.

Workflow:

Register → Activation Mail → Activate Account → Login

Password reset is supported via email.
