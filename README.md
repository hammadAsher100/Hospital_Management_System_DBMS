# 🏥 MediCore — Hospital Management System

A complete Flask-based Hospital Management System with SQL Server (SSMS) integration, role-based access control, and a modern Bootstrap 5 UI.

---

## 📦 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.10+, Flask 3.x           |
| ORM        | Flask-SQLAlchemy 3.x              |
| Database   | Microsoft SQL Server (SSMS)       |
| Auth       | Flask-Login + bcrypt              |
| Frontend   | Bootstrap 5.3, Chart.js 4.x       |
| Fonts      | DM Sans, DM Mono (Google Fonts)   |

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Microsoft SQL Server Express (or full) with SSMS
- ODBC Driver 17 for SQL Server → [Download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### 2. Clone & Install

```bash
git clone <your-repo>
cd hospital-management-system

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env .env.local
```

Edit `.env`:
```env
SECRET_KEY=your-super-secret-key-here
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=HMS_DB
# Leave DB_USERNAME and DB_PASSWORD blank for Windows Auth
```

### 4. Set Up Database

Open **SQL Server Management Studio (SSMS)** and run in order:

```sql
-- Step 1: Create schema
-- File: database/schema.sql

-- Step 2: Insert seed data
-- File: database/seed.sql
```

### 5. Fix Password Hashes

The seed.sql contains placeholder bcrypt hashes. Generate real ones:

```bash
python generate_hashes.py
```

Copy and run the printed UPDATE statements in SSMS.

### 6. Run the Application

```bash
python run.py
```

Open your browser: **http://localhost:5000**

---

## 👥 Default Login Credentials

| Username     | Password  | Role    |
|-------------|-----------|---------|
| `admin`     | `admin123`| Admin   |
| `dr_ahmed`  | `admin123`| Doctor  |
| `dr_fatima` | `admin123`| Doctor  |
| `nurse_sara`| `admin123`| Nurse   |
| `billing1`  | `admin123`| Billing |

> ⚠️ Change all passwords immediately in production!

---

## 🗂️ Project Structure

```
hospital-management-system/
├── app/
│   ├── __init__.py           # App factory
│   ├── models/               # SQLAlchemy models
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py         # Doctor + Nurse + DoctorSchedule
│   │   ├── appointment.py
│   │   ├── billing.py        # Bill + BillItem
│   │   ├── pharmacy.py       # Medicine + Prescription + PrescriptionItem
│   │   └── admission.py
│   ├── routes/               # Blueprint controllers
│   │   ├── auth.py           # /auth/*
│   │   ├── patients.py       # /patients/*
│   │   ├── appointments.py   # /appointments/*
│   │   ├── staff.py          # /staff/*
│   │   ├── billing.py        # /billing/*
│   │   ├── pharmacy.py       # /pharmacy/*
│   │   └── admin.py          # /admin/*
│   ├── templates/            # Jinja2 HTML
│   ├── static/               # CSS, JS
│   └── utils/                # Decorators
├── database/
│   ├── schema.sql            # Full DB schema
│   └── seed.sql              # Sample data
├── config.py
├── requirements.txt
├── generate_hashes.py
└── run.py
```

---

## 🔐 Role Permissions

| Feature              | Admin | Doctor | Nurse | Billing |
|---------------------|-------|--------|-------|---------|
| Dashboard           | ✅    | ✅     | ✅    | ✅      |
| View Patients       | ✅    | ✅     | ✅    | ✅      |
| Add/Edit Patients   | ✅    | ✅     | ✅    | ❌      |
| Delete Patients     | ✅    | ❌     | ❌    | ❌      |
| Book Appointments   | ✅    | ✅     | ✅    | ❌      |
| Complete/Cancel Appt| ✅    | ✅     | ❌    | ❌      |
| Generate Bills      | ✅    | ❌     | ❌    | ✅      |
| Record Payments     | ✅    | ❌     | ❌    | ✅      |
| Manage Pharmacy     | ✅    | ❌     | ❌    | ✅      |
| Create Prescriptions| ✅    | ✅     | ❌    | ❌      |
| Dispense Medicines  | ✅    | ❌     | ❌    | ✅      |
| Manage Staff        | ✅    | ❌     | ❌    | ❌      |
| View Reports        | ✅    | ❌     | ❌    | ❌      |

---

## 🧩 Core Modules

### 1. Patient Management
- Register, search, view, edit patients
- Tabbed patient profile: Info, Appointments, Prescriptions, Billing
- Allergy alerts and blood group tracking

### 2. Appointment System
- Book with real-time slot availability check (AJAX)
- Conflict detection (no double-booking)
- Status workflow: Scheduled → Completed / Cancelled
- Doctor schedule management (per day-of-week)

### 3. Billing Module
- Dynamic multi-item bill generation
- Partial payment support with balance tracking
- Printable invoice (print-optimized layout)
- CSV export

### 4. Pharmacy Module
- Medicine inventory with low stock alerts
- Prescription creation with multiple medicines
- One-click dispense with automatic stock reduction
- Expiry date tracking

### 5. Staff Management
- Doctor and nurse profiles
- Per-doctor weekly schedule builder
- User account activation/deactivation

### 6. Admin Dashboard & Reports
- Live stats: patients, appointments, revenue, low stock
- 7-day revenue chart (Chart.js)
- Patient demographics (gender, blood group)
- Appointment analytics by doctor and status
- Inventory value and low-stock report

---

## 🗄️ Database Connection

**Windows Authentication (Recommended):**
```
mssql+pyodbc://@localhost\SQLEXPRESS/HMS_DB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
```

**SQL Authentication (Fallback):**
Set `DB_USERNAME` and `DB_PASSWORD` in `.env`

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `pyodbc.InterfaceError` | Install ODBC Driver 17 from Microsoft |
| `Login failed for user` | Check Windows Auth settings or SQL Auth credentials |
| `Trusted_Connection fails` | Run as the same Windows user that has DB access |
| Password login fails | Run `generate_hashes.py` and update DB |
| Templates not found | Ensure you're running from project root |

---

## 📝 Production Checklist

- [ ] Change `SECRET_KEY` to a long random string
- [ ] Change all default passwords  
- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Restrict DB user permissions to HMS_DB only
- [ ] Set up HTTPS (use nginx + gunicorn)
- [ ] Configure regular database backups
- [ ] Remove debug mode (`debug=False` in run.py)
