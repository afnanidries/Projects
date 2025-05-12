# ☕ CoffeeMaker

A Spring Boot application for managing coffee recipes, inventory, and customer orders

## 🚀 Features

- Create, update, and delete coffee recipes  
- Manage ingredient inventory  
- Place and fulfill coffee orders  
- RESTful API architecture  

---

## 🛠️ Tech Stack

- Java 17  
- Spring Boot  
- Maven  
- JUnit (with EvoSuite, Randoop for test generation)  
- MySQL (optional for persistent storage)  
- Thymeleaf or REST front-end (depending on implementation)  

---

## 🧑‍💻 Getting Started

### 1. Clone the repository

git clone https://github.com/afnanidries/Projects.git  
cd Projects/CoffeeMaker

### 2. Build and run the application

chmod +x mvnw       # Only needed the first time  
./mvnw spring-boot:run

Or with standard Maven:

mvn spring-boot:run

### 3. Visit the app

Once started, open your browser:  
http://localhost:8080

---

## ✅ Running Tests

./mvnw test

Optional advanced testing:

- EvoSuite: Automated test generation  
- Randoop: Random test case generation  

---

## 📂 Project Structure

src/  
 └── main/  
     └── java/edu/ncsu/csc/CoffeeMaker/  
         ├── controllers/  
         ├── models/  
         ├── repositories/  
         ├── services/  
         └── CoffeeMakerApplication.java

---

## ✍️ Contributors

- Afnan Idries  

---
