# 🛍️ Ecommerce_API

A **FastAPI-based backend** for a modern e-commerce platform with secure authentication, encryption, and database integration.

---

## 🚀 Features

- 🔐 **User Authentication:** JWT-based login system with secure password hashing using `bcrypt`.
- 🧠 **Data Encryption:** Sensitive data protected with Fernet symmetric encryption.
- 🛒 **CRUD Operations:** APIs for managing users, products, orders, and order items.
- 🗄️ **Database Integration:** PostgreSQL database powered by SQLAlchemy ORM.
- 📘 **API Documentation:** Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).
- 🧩 **Modular Code Structure:** Well-organized architecture for scalability and clarity.

---

## 🛠️ Tech Stack

| Component | Technology Used |
|------------|-----------------|
| **Backend Framework** | FastAPI |
| **Language** | Python 3.13 |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Authentication** | JWT (via python-jose) |
| **Password Hashing** | Passlib (bcrypt) |
| **Encryption** | Cryptography (Fernet) |
| **Server** | Uvicorn |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/Ecommerce_API.git
cd Ecommerce_API
