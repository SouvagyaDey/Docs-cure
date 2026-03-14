# Docscure API Endpoints - Complete Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication Endpoints
- **POST** `/auth/login/` - Login (returns HTTP-only cookies)
- **POST** `/auth/signup/` - Register new user  
- **POST** `/auth/logout/` - Logout
- **GET** `/auth/user/` - Get current user profile
- **POST** `/auth/token-refresh/` - Refresh access token

## User Profiles
- **GET** `/profiles/` - List all profiles
- **GET** `/profiles/{id}/` - Get specific profile
- **PUT/PATCH** `/profiles/{id}/` - Update profile

## Doctors
- **GET** `/doctorappointment/doctors/` - List all doctors (5 doctors available)
- **GET** `/doctorappointment/doctors/{id}/` - Get doctor details
- **Permission**: AllowAny (public access)

Available Doctors:
1. Dr. John Smith - Cardiologist (15 years, ₹500)
2. Dr. Priya Patel - Neurologist (10 years, ₹600)
3. Dr. Rajesh Kumar - Orthopedist (12 years, ₹450)
4. Dr. Sarah Lee - Pediatrician (8 years, ₹400)
5. Dr. Amit Sharma - Dermatologist (7 years, ₹350)

Doctor Login: All doctors can login with:
- Email: dr.{lastname}@gmail.com (e.g., dr.smith@gmail.com)
- Password: doctor123

## Appointments
- **GET** `/doctorappointment/appointments/` - Get user's appointments
- **POST** `/doctorappointment/appointments/` - Create appointment
- **GET** `/doctorappointment/appointments/{id}/` - Get appointment details
- **Permission**: IsAuthenticated

## Doctor Reviews
- **GET** `/doctorappointment/doctor_reviews/` - List doctor reviews
- **POST** `/doctorappointment/doctor_reviews/` - Add review
- **Permission**: AllowAny (list), IsAuthenticated (create)

## Products
- **GET** `/products/product/` - List all products (21 products available)
- **GET** `/products/product/{id}/` - Get product details
- **Permission**: AllowAny for read, IsAdminUser for write

Available Products Categories:
- Medicines: Paracetamol, Ibuprofen, Amoxicillin, Cetirizine, Omeprazole
- Medical Equipment: Digital Thermometer, BP Monitor, Glucometer, Pulse Oximeter, Nebulizer, Stethoscope
- Health & Wellness: Multivitamin, Vitamin D3, Omega-3, Protein Powder, Calcium
- Fitness & Care: Yoga Mat, Resistance Bands, Foam Roller, Hand Sanitizer, Face Masks

## Product Stores
- **GET** `/products/productstore/` - List product stores
- **Permission**: AllowAny (read)

## Product Reviews
- **GET** `/products/productreview/` - List product reviews
- **POST** `/products/productreview/` - Add product review
- **Permission**: AllowAny (read), IsAuthenticated (write)

## Hospitals
- **GET** `/hospitalmanagement/hospitals/` - List hospitals
- **GET** `/hospitalmanagement/hospitals/{id}/` - Get hospital details
- **Permission**: AllowAny

## Hospital Reviews
- **GET** `/hospitalmanagement/hospitalreviews/` - List hospital reviews
- **Permission**: AllowAny

## Cart
- **GET** `/cart/carts/` - Get current cart
- **POST** `/cart/carts/` - Create cart
- **GET** `/cart/cart-items/` - List cart items
- **POST** `/cart/cart-items/` - Add item to cart
- **PATCH** `/cart/cart-items/{id}/` - Update cart item
- **DELETE** `/cart/cart-items/{id}/` - Remove from cart

## Orders
- **GET** `/orders/` - List user's orders
- **POST** `/orders/` - Create order (checkout)
- **GET** `/orders/{id}/` - Get order details
- **Permission**: IsAuthenticated

## Order Items
- **GET** `/orders/orderitem/` - List order items
- **GET** `/orders/orderitem/{id}/` - Get order item details

---

## Test Users

### Patients
- **Email**: user1@gmail.com
- **Password**: (ask admin)

### Doctors (All have password: doctor123)
- dr.smith@gmail.com - Cardiologist
- dr.patel@gmail.com - Neurologist
- dr.kumar@gmail.com - Orthopedist
- dr.lee@gmail.com - Pediatrician
- dr.sharma@gmail.com - Dermatologist

### Admin
- **Email**: admin@gmail.com
- **Password**: (ask admin)

---

## CORS Configuration
Frontend origins allowed:
- http://localhost:3000
- http://127.0.0.1:3000
- http://localhost:5173
- http://127.0.0.1:5173

## Notes
- All authentication uses HTTP-only cookies
- Frontend environment variable: `VITE_API_URL=http://localhost:8000/api`
- Database: MySQL with 21 products and 5 doctors
- All doctor endpoints are public (AllowAny)
- All product list/detail endpoints are public
- Appointments require authentication
