# Docs-cure Backend

Healthcare and e-commerce backend with Django REST Framework. Features doctor appointments, hospital management, products, orders, and cart with JWT authentication.

---

## Folder Structure

```
Docs-cure
├── authy/                  # Authentication, users, profiles
├── doctorappointment/      # Doctors, appointments, reviews
├── hospitalmanagement/     # Hospitals and reviews
├── products/               # Product catalog (MongoDB + MySQL)
├── orders/                 # Order management
├── cart/                   # Shopping cart
├── backend/                # Django settings and configuration
├── media/                  # User uploads (profile pictures, documents)
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SouvagyaDey/Docs-cure.git
```

### 2. Fork the Repository (Optional)

1. Go to https://github.com/SouvagyaDey/Docs-cure
2. Click **Fork** in the top right
3. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Docs-cure.git
   cd Docs-cure
   ```

---

## Database Setup with Docker

### 1. Start MySQL Container

```bash
docker run -d \
  --name docs_cure_mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=healthdoc \
  -p 3306:3306 \
  mysql:8.0
```

This creates a MySQL 8 container with:
- **Database**: `healthdoc` (matches settings.py)
- **User**: `root`
- **Password**: `root`
- **Port**: `3306`

### 2. Start MongoDB Container

```bash
docker run -d \
  --name docs_cure_mongodb \
  -p 27017:27017 \
  mongo:latest
```

This creates a MongoDB container with:
- **Database**: `product_db` (auto-created)
- **Port**: `27017`

### Verify Containers are Running

```bash
docker ps
```

You should see both `docs_cure_mysql` and `docs_cure_mongodb` containers running.

### Container Management

```bash
# Stop containers
docker stop docs_cure_mysql docs_cure_mongodb

# Start containers
docker start docs_cure_mysql docs_cure_mongodb

# Remove containers
docker rm -f docs_cure_mysql docs_cure_mongodb
```

---

## Run Development Server

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser --email admin@gmail.com
```

### 5. Start Dev Server

```bash
python manage.py runserver
```

Server runs at: **http://localhost:8000**

---

## 🗺️ API Routes

Base URL: `http://localhost:8000/api/`

### Authentication (`/api/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup/` | Register new user | No |
| POST | `/api/auth/login/` | Login (sets JWT cookies) | No |
| POST | `/api/auth/logout/` | Logout (clears cookies) | Yes |
| GET | `/api/auth/user/` | Get current user profile | Yes |
| POST | `/api/auth/isauthenticated/` | Check auth status | Yes |
| POST | `/api/auth/token-refresh/` | Refresh access token | Yes |

### User Profiles (`/api/profiles/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/profiles/` | List all profiles | No |
| GET | `/api/profiles/{id}/` | Get profile details | No |
| POST | `/api/profiles/` | Create profile | Yes (Admin) |
| PUT/PATCH | `/api/profiles/{id}/` | Update profile | Yes (Owner) |
| DELETE | `/api/profiles/{id}/` | Delete profile | Yes (Admin) |

### Doctors (`/api/doctorappointment/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/doctorappointment/doctors/` | List all doctors | No |
| GET | `/api/doctorappointment/doctors/{id}/` | Get doctor details | No |
| POST | `/api/doctorappointment/doctors/` | Create doctor profile | Yes (Doctor) |
| PUT/PATCH | `/api/doctorappointment/doctors/{id}/` | Update doctor | Yes (Owner/Admin) |
| DELETE | `/api/doctorappointment/doctors/{id}/` | Delete doctor | Yes (Owner/Admin) |

### Appointments (`/api/doctorappointment/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/doctorappointment/appointments/` | List appointments (filtered by role) | Yes |
| GET | `/api/doctorappointment/appointments/{id}/` | Get appointment details | Yes |
| POST | `/api/doctorappointment/appointments/` | Book appointment | Yes (Patient) |
| PUT/PATCH | `/api/doctorappointment/appointments/{id}/` | Update appointment | Yes (Doctor/Patient) |
| DELETE | `/api/doctorappointment/appointments/{id}/` | Cancel appointment | Yes (Admin) |

### Doctor Reviews (`/api/doctorappointment/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/doctorappointment/doctor_reviews/` | List doctor reviews | No |
| POST | `/api/doctorappointment/doctor_reviews/` | Add review | Yes |
| PUT/PATCH | `/api/doctorappointment/doctor_reviews/{id}/` | Update review | Yes (Owner/Admin) |
| DELETE | `/api/doctorappointment/doctor_reviews/{id}/` | Delete review | Yes (Owner/Admin) |

### Hospitals (`/api/hospitalmanagement/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/hospitalmanagement/hospitals/` | List all hospitals | No |
| GET | `/api/hospitalmanagement/hospitals/{id}/` | Get hospital details | No |
| POST | `/api/hospitalmanagement/hospitals/` | Add hospital | Yes (Admin) |
| PUT/PATCH | `/api/hospitalmanagement/hospitals/{id}/` | Update hospital | Yes (Admin) |
| DELETE | `/api/hospitalmanagement/hospitals/{id}/` | Delete hospital | Yes (Admin) |

### Hospital Reviews (`/api/hospitalmanagement/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/hospitalmanagement/hospitalreviews/` | List reviews | No |
| POST | `/api/hospitalmanagement/hospitalreviews/` | Add review | Yes |
| PUT/PATCH | `/api/hospitalmanagement/hospitalreviews/{id}/` | Update review | Yes (Owner/Admin) |
| DELETE | `/api/hospitalmanagement/hospitalreviews/{id}/` | Delete review | Yes (Owner/Admin) |

### Products (`/api/products/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/productstore/` | List all products | No |
| GET | `/api/products/productstore/{id}/` | Get product details | No |
| POST | `/api/products/productstore/` | Add product | Yes (Admin) |
| PUT/PATCH | `/api/products/productstore/{id}/` | Update product | Yes (Admin) |
| DELETE | `/api/products/productstore/{id}/` | Delete product | Yes (Admin) |

### Product Reviews (`/api/products/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/productreview/` | List reviews | No |
| POST | `/api/products/productreview/` | Add review | Yes |
| PUT/PATCH | `/api/products/productreview/{id}/` | Update review | Yes |
| DELETE | `/api/products/productreview/{id}/` | Delete review | Yes |

### Cart (`/api/cart/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart/carts/` | Get user's cart | Yes |
| POST | `/api/cart/carts/` | Create cart | Yes |
| GET | `/api/cart/cart-items/` | List cart items | Yes |
| POST | `/api/cart/cart-items/` | Add item to cart | Yes |
| PUT/PATCH | `/api/cart/cart-items/{id}/` | Update cart item | Yes |
| DELETE | `/api/cart/cart-items/{id}/` | Remove from cart | Yes |

### Orders (`/api/orders/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List user orders (Admin sees all) | Yes |
| GET | `/api/orders/{id}/` | Get order details | Yes |
| POST | `/api/orders/` | Create order | Yes |
| PUT/PATCH | `/api/orders/{id}/` | Update order | Yes (Owner/Admin) |
| DELETE | `/api/orders/{id}/` | Delete order | Yes (Admin) |

---

### Notes

- **Authentication**: Uses JWT cookies (httpOnly) for secure auth
- **Database**: MySQL for relational data, MongoDB for products (flexible schema)
- **Admin Panel**: Access at `http://localhost:8000/admin/`

---
