# 🏥 Hospital Management System

<div align="center">

<!-- Animated Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Hospital%20Management%20System&fontSize=40&fontColor=fff&animation=twinkling&fontAlignY=35&desc=A%20full-stack%20web%20application%20to%20digitize%20hospital%20operations&descAlignY=55&descSize=16" width="100%"/>

<br/>

![C#](https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=csharp&logoColor=white)
![.NET](https://img.shields.io/badge/.NET-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![Windows Forms](https://img.shields.io/badge/Windows_Forms-0078D4?style=for-the-badge&logo=windows&logoColor=white)

<br/>

A comprehensive desktop-based Hospital Management System built with **C# Windows Forms** and **Microsoft SQL Server** to streamline and digitize core hospital operations.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Modules](#-modules)
- [Tech Stack](#-tech-stack)
- [Database Design](#-database-design)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Team](#-team)

---

## 🌟 Overview

The Hospital Management System (HMS) is a full-featured desktop application designed to **digitize and streamline** the core operations of small to medium-sized hospitals and clinics. It replaces manual, paper-based hospital workflows with a centralized digital platform that ensures data integrity, efficiency, and ease of use.

The system covers everything from patient registration and doctor scheduling to pharmacy inventory and billing — all backed by a well-normalized relational database built on SQL Server.

---

## ✨ Features

- ✅ Register, update, and search patient records
- ✅ Manage doctor profiles, departments, and specializations
- ✅ Schedule and cancel patient appointments
- ✅ Track medicine inventory and issue prescriptions
- ✅ Generate invoices and process billing
- ✅ View comprehensive admin reports
- ✅ Data integrity enforced via SQL constraints, triggers, and stored procedures
- ✅ Full CRUD operations across all modules
- ✅ Clean, user-friendly Windows Forms interface

---

## 📦 Modules

### 1. 🧑‍⚕️ Patient Management
Handles the complete patient lifecycle within the hospital system.

- New patient registration with personal and medical details
- Update and delete patient records
- View full medical history per patient
- Search patients by ID, name, or CNIC
- Manage hospital admissions and discharges

---

### 2. 👨‍⚕️ Doctor & Appointment Management
Manages the hospital's medical staff and patient-doctor scheduling.

- Create and maintain doctor profiles
- Assign doctors to departments and specializations
- Schedule, reschedule, and cancel appointments
- View doctor availability by date and time slot
- Manage patient-doctor assignment records

---

### 3. 💊 Pharmacy & Inventory Management
Keeps track of all medicines and supplies within the hospital pharmacy.

- Add and update medicine stock records
- Issue medicines to patients against prescriptions
- Track medicine expiry dates with alerts
- Low-stock notification system
- Manage supplier information and purchase records

---

### 4. 🧾 Billing & Reports
Handles financial transactions and generates summary reports for administration.

- Generate itemized patient invoices
- Calculate consultation and pharmacy charges
- Process and record payments
- View billing history per patient
- Admin reports: daily revenue, patient statistics, inventory summaries

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | C# Windows Forms (.NET) |
| Backend / Logic | C# (OOP — Classes, Methods, Events) |
| Database | Microsoft SQL Server |
| Query Language | T-SQL (DDL, DML, TCL, stored procedures) |
| IDE | Visual Studio |
| DB Tool | SQL Server Management Studio (SSMS) |

---

## 🗄️ Database Design

The database is designed following proper relational database principles:

- **ER Modeling** — Entity-Relationship diagram with crow's foot notation
- **Normalization** — Schema normalized up to **BCNF**
- **Constraints** — Primary keys, foreign keys, NOT NULL, UNIQUE, CHECK
- **Stored Procedures** — Reusable SQL logic for critical operations
- **Transactions** — ACID-compliant operations for billing and inventory
- **Views** — Simplified data access for reporting

### Key Tables
