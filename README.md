# 🚀 EduAssign

### Professional Assignment Management System

**Enterprise Laravel MVC Academic Framework**

[![Developer](https://img.shields.io/badge/Developer-Ismail%20Benmbarek-blue.svg)](https://github.com/ismail-dz-16)
[![Stack](https://img.shields.io/badge/Backend-Laravel-E67E22.svg)](#)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1.svg)](#)


---

## 🌟 Project Executive Summary

**EduAssign** is a high‑performance web application engineered to digitize and streamline academic assignment workflows. It features a secure, dual‑portal experience enabling **Teachers** to design and manage assignments while **Students** submit and track their work with precision.

* **Core Pattern:** Model–View–Controller (MVC)
* **Architecture:** Monolithic Laravel with Eager Loading optimization
* **Security:** CSRF Protection, Bcrypt Password Hashing, Middleware Guards

---

## 🧱 Architecture Overview

| Layer           | Path                   | Responsibility                               |
| --------------- | ---------------------- | -------------------------------------------- |
| 🕹️ Controllers | `app/Http/Controllers` | Request handling & business logic flow       |
| 💾 Models       | `app/Models`           | Eloquent ORM entities & relationship mapping |
| 🎨 Views        | `resources/views`      | Dynamic UI rendering via Blade engine        |
| 🛣️ Routes      | `routes/web.php`       | Endpoint definitions & middleware filtering  |
| 🏗️ Migrations  | `database/migrations`  | Version‑controlled database schema           |

---

## ⚡ Key Capabilities

### 👨‍🏫 Instructor Module

* **Assignment Factory:** Create, update, and delete complex assignments
* **Submission Analytics:** Real‑time monitoring of submissions and timestamps
* **Dynamic Questions:** Support for multiple task formats and rich descriptions

### 🎓 Student Module

* **Work Portal:** Centralized dashboard for active and pending tasks
* **Digital Submission:** Secure uploads directly to instructor dashboards
* **Deadline Tracker:** Automatic status updates based on timelines

---

## 🛠️ Environment Prerequisites

Ensure your system meets the following requirements before setup:

* **PHP:** 8.2 or higher
* **Composer:** PHP dependency manager
* **Node.js & NPM:** Frontend asset compilation
* **Database:** MySQL 8.0+ or MariaDB
* **Web Server:** Apache, Nginx, or PHP built‑in server

---

## 🚀 Deployment Guide

### 1️⃣ Repository Acquisition

```bash
git clone https://github.com/ismail-dz-16/EduAssign.git
cd EduAssign
```

### 2️⃣ Dependency Installation

**Backend**

```bash
composer install
```

**Frontend**

```bash
npm install && npm run build
```

### 3️⃣ System Configuration

```bash
cp .env.example .env
php artisan key:generate
```

Edit `.env` and configure:

* `DB_DATABASE`
* `DB_USERNAME`
* `DB_PASSWORD`

### 4️⃣ Database Migration & Seeding

```bash
php artisan migrate --seed
```

### 5️⃣ Launch Application

```bash
php artisan serve
```

➡️ **Local URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛡️ Security & Integrity

* **Environment Protection:** `.env` excluded from version control
* **Role‑Based Access Control:** Laravel middleware & gates
* **Input Validation:** Form Requests prevent SQL injection & XSS

---

## 📄 License & Credits

* **Developer:** Ismail Benmbarek
* **Project Context:** Flagship Laravel MVC demonstration
* **License:** Open‑source for educational and development use

---

## 💡 Pro Tip

List all application routes and middleware bindings:

```bash
php artisan route:list
```

---

⭐ If you find this project useful, consider starring the repository on GitHub!
