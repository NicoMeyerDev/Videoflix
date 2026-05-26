# 📦 Videoflix Backend

Videoflix is a Netflix-style video streaming backend. Upload videos via the Django admin and the app will automatically convert them into HLS format (480p, 720p, 1080p) — ready to stream in any HLS-compatible player.

---

## 🛠️ Requirements

* [Docker](https://www.docker.com/)
* [Git](https://git-scm.com/)

---

## 🚀 Installation – Step by Step

### 1. Clone the repository

```
git clone (https://github.com/NicoMeyerDev/Videoflix)
cd "Videoflix Backend"
```

### 2. Set up environment variables

```
cp .env.template .env
```

Open `.env` and fill in your values. 

🔑 For Gmail you need an **App Password** – generate one at [Google Account Security](https://myaccount.google.com/security).

### 3. Start with Docker

```
docker-compose up --build -d
```

✅ The API will be available at `http://localhost:8000/`

---

## ⚙️ How it works

- Users register and receive an activation email before they can log in
- Authentication is handled via **JWT tokens** stored as **HttpOnly cookies**
- Uploaded videos are automatically converted to HLS format in the background via **Django RQ** + **ffmpeg**
- A thumbnail is automatically generated from the first second of the video
