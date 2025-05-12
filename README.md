# ☕ CoffeeMaker Application

A full-stack Spring Boot-based coffee shop app that supports customer orders, staff fulfillment, and manager oversight. Built with AngularJS on the frontend, MySQL as the database, and secure user authentication.

---

## 🙋 Getting Started

### 1. 📆 Clone the Repository

```bash
git clone https://github.com/afnanidries/Projects.git
cd Projects/CoffeeMaker
```

### 2. 🚀 Build and Run the Application

**Using Maven Wrapper (recommended):**

```bash
chmod +x mvnw   # Only needed the first time
./mvnw spring-boot:run
```

**Or with standard Maven:**

```bash
mvn spring-boot:run
```

### 3. 🌐 Visit the App

Once started, open your browser and visit:

[http://localhost:8080](http://localhost:8080)

---

## 👥 User Roles

- **Customer**: Place and view orders.
- **Staff**: Fulfill pending orders and manage inventory.
- **Manager**: Add/edit/remove staff and manage users.

---

## 🔧 Technologies Used

- **Java 11** + **Spring Boot** (MVC, Security, JPA)
- **MySQL** (with Hibernate ORM)
- **AngularJS** (1.6)
- **Thymeleaf** (for dynamic pages)
- **Maven** (project management)

---

## 🧭 Walkthrough: How to Use the App

### 📝 Register as a Customer
1. Click on **Register** from the homepage.
2. Fill in your desired **username** and **password**.
3. Upon successful registration, you'll be redirected to the login page.

![Register](docs/images/register.gif)

### 🔑 Log In
1. Enter your **username** and **password**.
2. Click **Log in** to be directed to your customer dashboard.

![Login](docs/images/login.gif)

### ☕ Place an Order
1. From the customer dashboard, browse available recipes.
2. Select your desired drinks and click **Place Order**.

![Place Order](docs/images/place-order.gif)

### 📦 Fulfillment by Staff
1. Staff logs in from their portal.
2. They can view all **pending orders**.
3. Select an order, enter payment received, and click **Fulfill Order**.
4. Inventory is updated automatically.

![Fulfill Order](docs/images/fulfill-order.gif)

### ✅ Order Completion
- Customers will see their order marked as **Ready for Pickup**.
- Once picked up, the order is archived and removed from the open queue.

![Order Ready](docs/images/order-ready.gif)

---

## ✨ Features

- **Login & Registration Flow**: Secure user authentication for customers, staff, and managers.
- **Order Creation**: Customers can browse recipes and place coffee orders.
- **Order Fulfillment**: Staff can view pending orders, process payments, and mark them as fulfilled.
- **Order History**: Completed orders are archived for tracking.
- **Staff Management Dashboard**: (in progress) Managers can add/edit/remove staff.
- **Inventory Management**: Inventory levels update automatically after order fulfillment.
- **UI Enhancements**: Modern styling with custom login/register pages.
- **RESTful API**: Backed by Spring Boot controllers and services for modular architecture.


---

## 💪 Contributors

- Afnan Idries — *Lead Developer*

---
