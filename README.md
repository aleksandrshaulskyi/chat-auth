# Chat-auth.

Authentication and session management for the distributed chat platform

The authentication microservice responsible for issuing, validating, refreshing, and managing stateless JWT-based sessions across the entire chat system.

## 🚀 Overview

Chat-auth handles all authentication workflows for the platform using a clean, stateless JWT approach.
It issues access tokens, refreshes them, and manages user sessions — while staying lightweight, fast, and isolated from other services.

The system embraces the benefits of JWT (simplicity, speed, no server-side storage) while also acknowledging their primary drawback:
already issued tokens cannot be instantly revoked.

To balance this, Chat-auth maintains session objects and provides structured workflows for issuing, refreshing, and terminating sessions.

The service operates with two domain entities:

- **User**

- **Session**

Everything related to authentication flows and user identity management lives here.

## 🧩 Features

**Create / Refresh / Terminate sessions**  
Full session lifecycle built around stateless JWT.

**User management (CRU)**  
Create, read, and update users.
(Delete operation is planned but not yet released.)

**Strict separation of responsibilities**  
Authentication concerns are isolated here — no mixing with transport or messaging layers.

## 🏗️ Architecture.

This microservice is built using the Clean Architecture approach.
It consists of 4 layers which are:

1) Domain (entities, value objects)
2) Application layer (domain entities orchestration and business logic)
3) Interface adapters (thin transport layer that incapsulates the internal logic)
4) Infrastructure (frameworks, databases, etc.)

## ⚙️ Usage.

1) Clone the repository.
2) Create .env file in the backed directory using the env_example.txt as an example.
3) ```docker-compose up --build``` in the directory where docker-compose.yaml file is located.
4) The application will be available on **http://localhost:8000**

## 📘 Docs.

Available at the standard FastAPI docs endpoint **http://localhost:8000/docs**

## 🔗 Back to the Main Index Repository

Explore the complete distributed chat system:
https://github.com/aleksandrshaulskyi/chat-index
