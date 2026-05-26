📦 Videoflix Backend
Videoflix is a Netflix-style video streaming backend built with Django 6.0.4 and Django REST Framework. Upload videos via the Django admin and the app will automatically convert them into HLS format (480p, 720p, 1080p) using ffmpeg — ready to stream in any HLS-compatible player.
🛠️ Requirements
Make sure the following is installed on your computer:

Docker
Git

ℹ️ The project runs entirely inside Docker containers. , Django 6.0.4, PostgreSQL, Redis, and ffmpeg are all installed automatically — no local installation needed.

🚀 Installation – Step by Step
1. Clone the repository
Open your terminal (or command prompt) and run:
git clone https://github.com/NicoMeyerDev/Videoflix
Then navigate into the project folder:
cd Videoflix
2. Set up environment variables
Copy the .env.template file and rename it to .env:

Windows

copy .env.template .env

Mac/Linux

<<<<<<< HEAD
### 1. Clone the repository

```
git clone https://github.com/NicoMeyerDev/Videoflix
cd "Videoflix Backend"
```

### 2. Set up environment variables

```
=======
>>>>>>> 667af55 (Update backend configuration and templates)
cp .env.template .env
Then open .env and fill in your values:
SECRET_KEY=your-secret-key

DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=your-db-password

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your@gmail.com

FRONTEND_URL=http://127.0.0.1:5500
🔑 For Gmail you need an App Password – generate one at Google Account Security.
3. Start with Docker
docker-compose up --build -d
✅ The API will then be available at:
http://localhost:8000/

ℹ️ The first build may take a few minutes as Docker installs all dependencies including ffmpeg.

⚙️ How it works

Users register and receive an activation email before they can log in
Authentication is handled via JWT tokens stored as HttpOnly cookies
Uploaded videos are automatically converted to HLS format (480p, 720p, 1080p) in the background via Django RQ + ffmpeg
A thumbnail is automatically generated from the first second of the video
