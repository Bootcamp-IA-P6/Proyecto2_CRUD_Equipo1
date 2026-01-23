# 📘 Proyecto2 – CRUD Movies API (FastAPI)

## 1. Introducción

Este proyecto consiste en el desarrollo de una **API REST CRUD** para la gestión de **películas, directores, géneros y usuarios**, implementada con **FastAPI**, **SQLAlchemy** y **MySQL**.

La API permite operaciones CRUD completas, soporte para **creación masiva (bulk)** y documentación automática mediante **Swagger**.

---

## 2. Tecnologías utilizadas

### 🔹 FastAPI

Framework web moderno para Python, orientado a APIs REST, con tipado fuerte y documentación automática.

### 🔹 MySQL

Sistema gestor de bases de datos relacional utilizado para persistencia.

### 🔹 MySQL Workbench

Herramienta gráfica para administrar bases de datos MySQL.

**Versión usada**:  
MySQL Workbench 8.0.44 CE (64 bits)

### 🔹 Postman

Cliente para pruebas manuales de APIs HTTP.

**Versión usada**:  
Postman for Windows 11.81.0 (x64)

---

## 3. Descarga de herramientas

- **MySQL + Workbench**:  
    MySQL Community Server + MySQL Workbench 8.0 (Oracle)
    
- **Postman**:  
    Postman Desktop App for Windows (x64)
    

---

## 4. Clonado del repositorio y ramas

```
git clone https://github.com/Bootcamp-IA-P6/Proyecto2_CRUD_Equipo1.git
cd Proyecto2_CRUD_Equipo1
git switch develop
```

---

## 5. Preparación del entorno virtual

```
python -m venv .venv
#Windows
source .venv/Scripts/activate
```

---

## 6. Instalación de dependencias

```
pip install -r requirements.txt
pip list
```

---

## 7. Variables de entorno

`cp .env.example .env`

Editar `.env` con los datos locales de MySQL.

---

## 8. Base de datos

1. Abrir **MySQL Workbench**
    
2. Conectarse al servidor local
    
3. Crear la base de datos:
    

```sql
CREATE DATABASE db_movies_ai;
```

---

## 9. Ejecución del proyecto

```
uvicorn main:app --reload
```

Salida esperada:

`Uvicorn running on http://127.0.0.1:8000`

---

## 10. Documentación Swagger (FastAPI)

FastAPI genera documentación automáticamente.

### 📄 Swagger UI

`http://127.0.0.1:8000/docs`

### ¿Por qué `/docs`?

- Permite **ver todos los endpoints**
    
- Probar métodos **GET / POST / PUT / PATCH / DELETE**
    
- Validar esquemas y payloads
    
- Sustituye temporalmente a Postman
    

Ruta alternativa:

`http://127.0.0.1:8000/redoc`

---

## 11. Estructura del proyecto

```tree
Proyecto2_CRUD_Equipo1-develop/
├── .env.example
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
├── docs/
│   └── der_moviesAi.png
└── src/
    ├── __init__.py
    ├── config/
    │   └── config_variables.py
    ├── controllers/
    │   ├── directores_controller.py
    │   ├── genero_controller.py
    │   ├── peliculas_controller.py
    │   └── users_controller.py
    ├── database/
    │   ├── base.py
    │   └── database.py
    ├── models/
    │   ├── peliculas_models.py
    │   └── users_model.py
    ├── routes/
    │   ├── directores_routes.py
    │   ├── genero_routes.py
    │   ├── peliculas_routes.py
    │   └── user_routes.py
    ├── schemas/
    │   ├── directores_schemas.py
    │   ├── genero_schemas.py
    │   ├── peliculas_schemas.py
    │   └── users_schemas.py
    └── utils/
        └── security.py
```

Código fuente y txt.

[ArchivosBase](ArchivosBase.md)

---

## 12. Descripción del código (outline)

### `main.py`

- Punto de entrada de la aplicación
    
- Inicializa FastAPI
    
- Registra routers
    
- Configura middleware
    

---

### `src/models/`

Define los **modelos ORM (SQLAlchemy)**:

- `Director`
    
- `Genero`
    
- `Pelicula`
    
- `User`
    
- Tablas intermedias
    

---

### `src/schemas/`

Define los **schemas Pydantic**:

- Validación de datos de entrada
    
- Separación Create / Update / Response
    
- Control de serialización
    

---

### `src/controllers/`

Contiene la **lógica de negocio**:

- CRUD individual
    
- CRUD bulk
    
- Validaciones
    
- Acceso a base de datos
    

---

### `src/routes/`

Define los **endpoints REST**:

- `/directores`
    
- `/peliculas`
    
- `/generos`
    
- `/users`
    
- Endpoints bulk (`/bulk`)
    

---

### `src/database/`

- Configuración de SQLAlchemy
    
- Sesiones de base de datos
    
- Base declarativa
    

---

### `src/utils/`

- Seguridad
    
- Hash de contraseñas
    
- Utilidades auxiliares
    

---

## 13. Pruebas con Postman

- Métodos HTTP:
    
    - `GET`
        
    - `POST`
        
    - `PUT`
        
    - `PATCH`
        
    - `DELETE`
        
    - `HEAD`
        
    - `OPTIONS`
        
- Uso de JSON
    
- Pruebas de endpoints bulk
    
- Validación de errores (`404`, `422`, `500`)
    

---

## 14. Buenas prácticas aplicadas

- Arquitectura por capas
    
- Separación de responsabilidades
    
- Variables de entorno
    
- Bulk endpoints
    
- Swagger integrado
    
- ZIP limpio para entrega
    

---

## 15. Conclusión

El proyecto implementa una **API REST completa**, extensible y bien estructurada, cumpliendo criterios técnicos de backend moderno con FastAPI y SQLAlchemy, preparada tanto para desarrollo como para evaluación académica o técnica.