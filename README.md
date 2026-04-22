<h1 align="center">
  📝 BridgeLang Blog
</h1>

<p align="center">
  <strong>A full-featured Django blog platform with authentication, SEO, and Docker support</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-4.2_LTS-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-22c55e" alt="License">
</p>

---

## 📖 About

**BridgeLang Blog** is a standalone blog platform built with Django, designed to deliver a complete content publishing experience. It includes a rich text editor, category and tag management, a comment moderation system, SEO tooling, and a customized admin panel — all secured with CAPTCHA authentication and environment-based configuration.

> Built as a portfolio project. The codebase is structured to be extensible — the lesson/course module is scaffolded and ready for future development.

---

## 🎯 Purpose

- This project was built as a portfolio to showcase:

- Django project architecture (multi-settings pattern)

- Secure authentication and form handling

- Docker-based deployment workflow

- Clean, maintainable, and extensible code structure

---

## 📸 Screenshots

> _Add screenshots here_

```
BridgeLang/BridgeLang/static/img/Screenshot1.png
BridgeLang/BridgeLang/static/img/Screenshot2.png
BridgeLang/BridgeLang/static/img/Screenshot3.png

```

---

## ✨ Features

### 📝 Blog System
- **Rich Text Editor** — Summernote editor for content creation
- **Categories & Tags** — Organize posts with categories and `django-taggit`
- **Comment System** — User comments with admin approval workflow
- **Search** — Case-insensitive search across posts
- **Pagination & Filtering** — Filter posts by author, category, and tag
- **View Counter** — Track post popularity with view counts
- **Login-Required Posts** — Restrict specific posts to authenticated users only

### 🔐 Authentication & Security
- **Email or Username Login** — Custom authentication backend
- **CAPTCHA Protection** — On both login and registration forms
- **CSRF/XSS Protection** — Django's built-in headers + additional hardening
- **Environment Variables** — All secrets managed via `python-decouple`

### 🛠 Admin & SEO
- **Customized Admin Panel** — Author-scoped permissions, Summernote editor, inline editing
- **XML Sitemap** — Auto-generated sitemap for search engines
- **Robots.txt** — Configurable via `django-robots`
- **Maintenance Mode** — Toggle with superuser bypass
- **Custom Error Pages** — Branded 400, 403, 404, and 500 pages

---

## 🏗 Architecture

```
BridgeLang/
├── CoreFolder/                  # Project settings, URLs, error handlers
│   ├── settings/
│   │   ├── base.py              # Shared configuration
│   │   ├── development.py       # Dev: SQLite, debug toolbar, console email
│   │   └── production.py        # Prod: PostgreSQL, SMTP, SSL/HSTS
│   ├── urls.py                  # Root URL routing
│   └── errors.py                # Custom error handlers (400–500)
│
├── AppFolder/                   # Core site (homepage, contact, newsletter)
│   ├── models.py                # Contact & Newsletter models
│   ├── views.py                 # Homepage, contact form, newsletter signup
│   ├── sitemaps.py              # Static page sitemap
│   └── tests.py
│
├── BlogFolder/                  # Blog application
│   ├── models.py                # Post, Category, Comment models
│   ├── views.py                 # Blog listing, detail, search
│   ├── admin.py                 # Custom admin with author-scoped permissions
│   ├── templatetags/            # Custom template tags
│   └── tests.py
│
├── AccountsFolder/              # Authentication
│   ├── backends.py              # Email/Username auth backend
│   ├── forms.py                 # Registration & login forms with CAPTCHA
│   ├── views.py                 # Login, logout, signup views
│   └── tests.py
│
├── LessonsFolder/               # 🚧 Scaffolded — planned for future release
│   ├── models.py                # Course, Lesson, UserProgress models
│   ├── views.py
│   ├── admin.py
│   └── tests.py
│
├── templates/                   # Django templates (base + app-specific)
├── static/                      # CSS, JS, vendor libraries, images
├── Dockerfile                   # Multi-stage production Docker image
├── docker-compose.yml           # Full stack: Django + PostgreSQL + smtp4dev
├── requirements.txt
└── .env.example                 # Environment variable template
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip
- PostgreSQL 16 (production) or SQLite (development)
- Docker & Docker Compose *(optional)*

---

### Option 1: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/alikavianifar/BridgeLang.git
cd BridgeLang

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Open .env and fill in your values (SECRET_KEY, database, email, etc.)

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### Option 2: Docker

```bash
# 1. Clone and configure
git clone https://github.com/alikavianifar/BridgeLang.git
cd BridgeLang
cp .env.example .env
# Open .env and fill in your values

# 2. Build and start all services
docker compose up --build

# 3. In a new terminal — run migrations and create superuser
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Visit [http://localhost:8000](http://localhost:8000)

**With development email server (smtp4dev):**
```bash
docker compose --profile dev up --build
# smtp4dev UI → http://localhost:5000
```

---

## 🧪 Running Tests

### Local Development

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test AppFolder
python manage.py test BlogFolder
python manage.py test AccountsFolder

# Run with detailed output
python manage.py test -v 2
```

### Docker

```bash
# Run all tests inside the container
docker compose exec web python manage.py test

# Run tests for a specific app
docker compose exec web python manage.py test BlogFolder

# Run with detailed output
docker compose exec web python manage.py test -v 2
```

---

## ⚙️ Environment Variables

All sensitive configuration is managed through environment variables. Copy `.env.example` to `.env` and fill in your values.

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key *(generate a strong one)* | `openssl rand -base64 50` |
| `DEBUG` | Enable debug mode | `True` / `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `PGDB_NAME` | PostgreSQL database name | `bridgelang_db` |
| `PGDB_USER` | PostgreSQL username | `postgres` |
| `PGDB_PASSWORD` | PostgreSQL password | `yourpassword` |
| `PGDB_HOST` | PostgreSQL host | `localhost` |
| `PGDB_PORT` | PostgreSQL port | `5432` |
| `EMAIL_HOST` | SMTP server host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP server port | `587` |
| `EMAIL_HOST_USER` | SMTP username / email address | `you@gmail.com` |
| `EMAIL_HOST_PASSWORD` | SMTP password or app password | `yourpassword` |
| `CONTACT_RECIPIENTS` | Contact form notification recipients | `admin@example.com` |
| `USE_SSL_CONFIG` | Enable HTTPS/HSTS in production | `False` |
| `MAINTENANCE_MODE` | Enable maintenance mode | `False` |

---

## 🛡 Security

This project follows Django security best practices:

- ✅ **No secrets in source code** — All sensitive data loaded from `.env`
- ✅ **CSRF protection** — Enabled on all forms
- ✅ **XSS protection** — `Content-Type` nosniff + browser XSS filter headers
- ✅ **Clickjacking protection** — `X-Frame-Options` header
- ✅ **SSL/HSTS** — Configurable HTTPS enforcement with HSTS preload
- ✅ **CAPTCHA** — Bot protection on login and registration
- ✅ **Password validation** — Django's built-in validators
- ✅ **Debug toolbar** — Only loaded in development mode
- ✅ **Comment security** — Post assignment handled server-side, not via form input

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 4.2 LTS, Python 3.12 |
| **Database** | PostgreSQL 16 (prod), SQLite (dev) |
| **Frontend** | Bootstrap 5, AOS.js, Swiper.js, GLightbox |
| **Rich Text** | Summernote Editor |
| **Auth** | Custom Email/Username Backend + django-simple-captcha |
| **SEO** | Django Sitemaps, django-robots |
| **Deployment** | Docker, Gunicorn, Nginx |
| **Config** | python-decouple |
| **Security** | SSL/HSTS, CSRF, XSS headers |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).