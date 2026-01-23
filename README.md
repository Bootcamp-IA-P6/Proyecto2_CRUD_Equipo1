# 🎬 Backend API – CRUD de Películas

Este proyecto es una **API REST desarrollada con FastAPI**, orientada a la gestión de **películas, géneros, directores y usuarios**, aplicando buenas prácticas de arquitectura, manejo de errores, documentación profesional y testing.

Forma parte de un sistema CRUD completo, pensado para trabajo en equipo, escalabilidad y entornos reales de desarrollo backend.

---

## 🚀 Tecnologías utilizadas

* **Python 3.11+**
* **FastAPI** – Framework principal
* **SQLAlchemy** – ORM
* **Pydantic** – Validación y serialización de datos
* **Uvicorn** – Servidor ASGI
* **Passlib (bcrypt)** – Hashing seguro de contraseñas
* **Email-validator** – Validación de emails
* **Pytest** – Testing automático
* **Swagger / OpenAPI** – Documentación automática

---

## 🧱 Arquitectura del proyecto

El backend sigue una arquitectura modular y limpia:

```
src/
│
├── controllers/     # Lógica de negocio
├── routes/          # Endpoints de la API
├── schemas/         # Validación de datos (Pydantic)
├── models/          # Modelos de base de datos
├── database/        # Configuración de la base de datos
├── utils/           # Utilidades (seguridad, hashing)
├── tests/           # Tests automáticos (pytest)
└── main.py          # Punto de entrada de la aplicación
```

### ✔ Beneficios de esta arquitectura

* Separación clara de responsabilidades
* Código mantenible y escalable
* Facilita testing y trabajo en equipo
* Preparado para crecimiento del proyecto

---

## ⚙️ Instalación y ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Proyecto2_CRUD_Equipo1
```

### 2️⃣ Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

📌 **Importante**
El archivo `requirements.txt` incluye todas las librerías necesarias para:

* FastAPI y SQLAlchemy
* Validación de datos
* Hashing de contraseñas
* Testing con pytest

---

### 4️⃣ Ejecutar el servidor

```bash
uvicorn src.main:app --reload
```

La API estará disponible en:

```
http://127.0.0.1:8000
```

---

## 📚 Documentación de la API (Swagger)

La API cuenta con documentación automática mediante **Swagger**:

* 🔗 **Swagger UI**

```
http://127.0.0.1:8000/docs
```

* 🔗 **OpenAPI JSON**

```
http://127.0.0.1:8000/openapi.json
```

Incluye:

* Todos los endpoints disponibles
* Métodos HTTP
* Esquemas de request y response
* Códigos de estado documentados
* Mensajes de error claros

---

## 🚨 Manejo de errores

El proyecto implementa un manejo de errores profesional y consistente:

| Código | Descripción                          |
| ------ | ------------------------------------ |
| 200    | OK                                   |
| 201    | Recurso creado correctamente         |
| 204    | Eliminación correcta (sin contenido) |
| 404    | Recurso no encontrado                |
| 409    | Conflicto (datos duplicados)         |
| 422    | Error de validación                  |

Los errores se gestionan desde los **controllers** y están documentados en Swagger.

---

## 🗑️ Soft Delete (Usuarios)

Los usuarios **no se eliminan físicamente** de la base de datos.

✔ Se aplica **Soft Delete** (`is_active = false`)
✔ Evita la pérdida de información
✔ Permite auditoría y recuperación
✔ Práctica habitual en sistemas reales

Por este motivo, un usuario eliminado puede seguir apareciendo en consultas generales si no se filtra por estado.

---

## 🧪 Testing con Pytest

El proyecto incluye **tests automáticos** desarrollados con **pytest**, enfocados en validar el correcto funcionamiento de los endpoints.

📂 Los tests se encuentran en:

```
src/tests/
```

### ✔ ¿Qué se testea?

* Creación de recursos (POST)
* Listado de recursos (GET)
* Eliminación lógica (DELETE)
* Manejo correcto de errores (`404`, `409`, `422`)
* Respuestas HTTP esperadas

### ▶️ Ejecutar los tests

```bash
pytest
```

📌 El uso de tests permite:

* Detectar errores tempranamente
* Garantizar estabilidad del código
* Facilitar refactorizaciones
* Cumplir estándares profesionales

---

## 🧪 Estado del proyecto

✅ CRUD completo
✅ Documentación Swagger
✅ Manejo de errores estandarizado
✅ Arquitectura escalable
✅ Tests automáticos con pytest
✅ Trabajo con ramas y Pull Requests

---

## 📌 Próximas mejoras

* Autenticación con JWT
* Roles y permisos
* Filtros por estado (`is_active`)
* Cobertura de tests más avanzada
* Dockerización

---

## ✨ Equipo

Proyecto desarrollado como parte de un proceso formativo en backend con **FastAPI**, aplicando buenas prácticas de desarrollo profesional, control de versiones, testing y trabajo colaborativo.
