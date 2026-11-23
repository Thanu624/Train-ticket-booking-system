# 🚂 RailBook Pro — Train Ticket Booking System

A full-stack train ticket booking system built with **React.js + FastAPI + SQLite (MySQL-ready)**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, React Router v6, Axios |
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.x, Pydantic v2 |
| Database | SQLite (dev) / MySQL 8 (prod via docker-compose) |
| Auth | JWT (HS256), bcrypt, Role-based (USER / ADMIN) |

---

## Quick Start

### 1. Backend Setup

```powershell
# From project root
cd backend
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env — set USE_SQLITE=True for local dev (default)

# Seed database (creates tables + sample data)
$env:PYTHONPATH='..'; python seed.py

# Start server
$env:PYTHONPATH='..'; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Backend available at:** http://127.0.0.1:8000  
**Swagger docs:** http://127.0.0.1:8000/docs

### 2. Frontend Setup

```powershell
# From project root
cd frontend
npm install
npm run dev
```

**Frontend available at:** http://127.0.0.1:5173

---

## Demo Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@railbook.com | Admin@123 |
| User | pattbhi@railbook.com | Pattbhi@123 |

---

## Environment Variables (backend/.env)

```env
# Database
USE_SQLITE=True          # True for SQLite, False for MySQL
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/train_booking

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# App
APP_NAME=RailBook Pro
DEBUG=True
```

---

## Running with MySQL (Docker)

```powershell
# Start MySQL container
docker-compose up -d

# Set in backend/.env:
USE_SQLITE=False
DATABASE_URL=mysql+pymysql://railbook_user:railbook_pass@localhost:3306/train_booking

# Run Alembic migrations
cd backend
$env:PYTHONPATH='..'; alembic upgrade head

# Seed
$env:PYTHONPATH='..'; python seed.py
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /api/v1/auth/register | Register user | Public |
| POST | /api/v1/auth/login | Login → JWT | Public |
| GET | /api/v1/auth/me | Current user | User |
| GET | /api/v1/trains | List all trains | Public |
| GET | /api/v1/trains/search | Search trains | Public |
| POST | /api/v1/trains | Add train | Admin |
| PUT | /api/v1/trains/{id} | Update train | Admin |
| DELETE | /api/v1/trains/{id} | Delete train | Admin |
| GET | /api/v1/train-classes/train/{id} | Get classes for train | Public |
| POST | /api/v1/train-classes | Add class | Admin |
| DELETE | /api/v1/train-classes/{id} | Delete class | Admin |
| GET | /api/v1/passengers | List passengers | User |
| POST | /api/v1/passengers | Add passenger | User |
| POST | /api/v1/tickets/book | Book ticket | User |
| GET | /api/v1/tickets/my-bookings | My tickets | User |
| GET | /api/v1/tickets/pnr/{pnr} | PNR lookup | Public |
| POST | /api/v1/tickets/{id}/cancel | Cancel ticket | User |
| POST | /api/v1/payments/process | Process payment | User |

---

## Running Tests

```powershell
# From project root
$env:PYTHONPATH='backend'; $env:TESTING='1'
.\backend\.venv\Scripts\python.exe -m pytest backend/tests/ -c backend/pytest.ini -v
```

---

## Project Structure

```
thanoosha_ticket booking/
├── backend/
│   ├── app/
│   │   ├── config/        # settings, DB session, security, auth deps
│   │   ├── controllers/   # FastAPI routers
│   │   ├── services/      # interfaces + implementations
│   │   ├── repositories/  # data access layer
│   │   ├── entities/      # SQLAlchemy models
│   │   ├── dtos/          # Pydantic schemas
│   │   ├── enums/         # ClassType, TicketStatus, etc.
│   │   ├── exceptions/    # custom exceptions + handlers
│   │   └── utils/         # PNR generator, seat allocator
│   ├── alembic/           # DB migrations
│   ├── tests/             # pytest tests
│   ├── seed.py            # database seeder
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── src/
│       ├── api/           # Axios API clients
│       ├── context/       # AuthContext
│       ├── pages/         # All pages (Login, Home, Search, Booking, etc.)
│       ├── routes/        # AppRoutes, ProtectedRoute, AdminRoute
│       └── components/    # Layout (sidebar + topbar)
├── docker-compose.yml
└── README.md
```
