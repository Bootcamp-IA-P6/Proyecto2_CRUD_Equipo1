# 🎥 Movie Catalog API – Backend

RESTful API for managing a movie catalog with authentication, roles, image upload and relational data.

Este repositorio contiene el backend de una aplicación de catálogo de películas desarrollado con **FastAPI**, **SQLAlchemy** y **MySQL**.  
La API permite gestionar usuarios, películas, directores y géneros, incluyendo autenticación JWT, control de acceso por roles y subida de imágenes.

---

## ✨ Características principales

- ⚡ API REST moderna con FastAPI
- 🔐 Autenticación JWT (OAuth2 Password Flow)
- 👤 Gestión de usuarios con roles (admin / cliente)
- 🎬 CRUD completo de películas
- 🎭 Gestión de directores y géneros
- 🧩 Relación many-to-many (películas ↔ géneros)
- 🖼️ Subida y recuperación de imágenes
- 📦 Operaciones en bloque (bulk)
- 🔒 Contraseñas cifradas con bcrypt

---

## 🧑‍💻 Tecnologías utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- Uvicorn
- bcrypt
- python-jose (JWT)
- pytest

---

## 🏗️ Arquitectura del proyecto

```
backend/
├── src/
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Esquemas Pydantic
│   ├── controllers/     # Lógica de negocio
│   ├── routes/          # Endpoints de la API
│   ├── database/        # Sesión y conexión a la BD
│   ├── config/          # Configuración y entorno
│   └── utils/           # Seguridad y utilidades
├── tests/               # Tests automatizados (pytest)
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_generos.py
│   ├── test_directores.py
│   └── test_peliculas.py
├── uploads/             # Imágenes subidas
├── main.py              # Entry point
├── requirements.txt
└── .env
```

---

## 🔁 Flujo de la aplicación

```
Client (Frontend / Swagger)
           ↓
    FastAPI Routes
           ↓
  Controllers (CRUD)
           ↓
  SQLAlchemy Models
           ↓
    MySQL Database
```

---

## 🔐 Autenticación

La API implementa **OAuth2 Password Flow con JWT**.

### Flujo de autenticación

1. Crear usuario
2. Login en `/token`
3. Recibir `access_token`
4. Usar el token en endpoints protegidos

```
Authorization: Bearer <access_token>
```

### Roles

- **Admin** → acceso total
- **Cliente** → acceso limitado

---

## 📌 Endpoints disponibles

### 🔑 Authentication

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/token` | Login y obtención de token |

### 👤 Users

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Crear usuario |
| GET | `/api/v1/users/` | Obtener usuarios |
| GET | `/api/v1/users/{user_id}` | Obtener usuario |
| PATCH | `/api/v1/users/{user_id}` | Actualizar usuario |
| DELETE | `/api/v1/users/{user_id}` | Eliminar usuario |

### 🎭 Géneros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/generos/` | Obtener géneros |
| POST | `/api/v1/generos/` | Crear género |
| GET | `/api/v1/generos/{genero_id}` | Obtener género |
| PUT | `/api/v1/generos/{genero_id}` | Actualizar género |
| DELETE | `/api/v1/generos/{genero_id}` | Eliminar género |

### 🎬 Directores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/directores/` | Crear director |
| GET | `/api/v1/directores/` | Obtener directores |
| POST | `/api/v1/directores/bulk` | Crear directores en bloque |
| GET | `/api/v1/directores/{director_id}` | Obtener director |
| PATCH | `/api/v1/directores/{director_id}` | Actualizar director |
| DELETE | `/api/v1/directores/{director_id}` | Eliminar director |

### 🎥 Películas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/peliculas/upload` | Subir imagen |
| GET | `/api/v1/peliculas/imagen/{filename}` | Obtener imagen |
| GET | `/api/v1/peliculas/` | Obtener películas (público) |
| POST | `/api/v1/peliculas/` | Crear película |
| POST | `/api/v1/peliculas/bulk` | Crear películas en bloque |
| GET | `/api/v1/peliculas/{pelicula_id}` | Obtener película |
| PATCH | `/api/v1/peliculas/{pelicula_id}` | Actualizar película |
| DELETE | `/api/v1/peliculas/{pelicula_id}` | Eliminar película |

---

## 🧪 Tests automatizados

El backend cuenta con **tests implementados con pytest** para verificar el correcto funcionamiento de los principales endpoints.

### 📂 Ubicación

```
backend/tests/
```

### 🧠 Qué se testea

- 👤 **Usuarios:**
  - Creación
  - Lectura
  - Actualización
  - Eliminación

- 🎭 **Géneros:**
  - Crear
  - Listar
  - Eliminar

- 🎬 **Directores:**
  - Crear
  - Listar
  - Operaciones bulk

- 🎥 **Películas:**
  - CRUD completo
  - Relaciones con géneros y directores

### ▶️ Ejecución de los tests

Desde la carpeta `backend`:

```bash
pytest
```

Los tests se ejecutan de forma aislada y no afectan los datos reales del entorno de desarrollo.

---

## 🖼️ Gestión de imágenes

- Subida mediante `multipart/form-data`
- Almacenamiento en el servidor
- Recuperación mediante endpoint dedicado

Permite asociar imágenes (posters) a las películas.

---

## ⚙️ Variables de entorno

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=movie_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
```

---

## ▶️ Ejecución del proyecto

```bash
uvicorn main:app --reload
```

### 📍 API

```
http://127.0.0.1:8000
```

### 📘 Swagger

```
http://127.0.0.1:8000/docs
```

---

## 🗄️ Base de datos

- Tablas creadas automáticamente al iniciar
- Relaciones gestionadas por SQLAlchemy
- Validación de claves foráneas antes de asignación

---

## 🧠 Buenas prácticas aplicadas

- Separación de capas (routes / controllers / models)
- Validación con Pydantic
- Endpoints protegidos por roles
- Operaciones bulk controladas
- Uso de PATCH para updates parciales

---

✨ **Backend desarrollado con FastAPI, SQLAlchemy y criterio técnico.**
