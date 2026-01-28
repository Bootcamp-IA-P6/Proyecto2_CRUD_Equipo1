# 🎬 Movie Catalog App

**Full-Stack Movie Management Platform**

Aplicación web full-stack para la gestión de un catálogo de películas, con autenticación, roles, subida de imágenes y relaciones complejas entre entidades.

---

## 🌟 Visión general

**Movie Catalog App** es una aplicación web desarrollada con una arquitectura moderna **Frontend + Backend desacoplados**, pensada para demostrar buenas prácticas en desarrollo full-stack.

Incluye:

- Panel público para visualizar películas
- Panel de administración protegido
- API REST robusta y documentada
- Gestión avanzada de datos relacionales
- Subida y consumo de imágenes sin almacenarlas en la base de datos

---

## 🧩 Arquitectura general

```
┌──────────────┐  HTTP / JSON  ┌──────────────────┐
│   Frontend   │ ───────────────────────▶ │     Backend      │
│ (HTML / JS)  │                │ FastAPI + ORM    │
└──────────────┘                └─────────┬────────┘
                                          │
                                          ▼
                                  ┌────────────┐
                                  │   MySQL    │
                                  └────────────┘
```

---

## ✨ Funcionalidades principales

### 👥 Usuarios y seguridad

- Registro y login de usuarios
- Autenticación con JWT
- Control de acceso por roles
- Rutas protegidas para administradores

### 🎬 Catálogo de películas

- Crear, editar, eliminar y listar películas
- Asociación con director y múltiples géneros
- Visualización pública del catálogo

### 🖼️ Imágenes

- Subida de posters desde el frontend
- Almacenamiento en el servidor (no en la BD)
- Consumo de imágenes vía endpoint dedicado

### 📦 Gestión avanzada

- Operaciones bulk (directores y películas)
- CRUD completo de géneros y directores
- Interfaz de administración intuitiva

---

## 🧑‍💻 Tecnologías utilizadas

### Backend

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- JWT (OAuth2 Password Flow)
- bcrypt
- Uvicorn
- pytest

### Frontend

- HTML5
- CSS3
- JavaScript (Vanilla)
- Bootstrap
- SweetAlert2
- Fetch API

---

## 📁 Estructura del proyecto

```
Proyecto2_CRUD_Equipo1/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── controllers/
│   │   ├── routes/
│   │   ├── database/
│   │   ├── config/
│   │   └── utils/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_users.py
│   │   ├── test_generos.py
│   │   ├── test_directores.py
│   │   └── test_peliculas.py
│   ├── uploads/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── admin.js
│   │   ├── auth.js
│   │   ├── catalogo.js
│   │   └── common.js
│   ├── admin_panel.html
│   ├── index.html
│   ├── login.html
│   └── .env
│
└── README.md
```

---

## 🔐 Autenticación y roles

La aplicación utiliza **JWT** para la autenticación.

### Flujo

1. El usuario inicia sesión
2. El backend devuelve un `access_token`
3. El token se guarda en `localStorage`
4. Las peticiones protegidas lo envían en headers

```
Authorization: Bearer <access_token>
```

### Roles

- **admin** → acceso total (panel admin)
- **user** → acceso público

---

## 📡 Backend – API REST

### 📘 Documentación interactiva (Swagger)

```
http://127.0.0.1:8000/docs
```

### Endpoints destacados

- `/token` → login
- `/api/v1/users/` → usuarios
- `/api/v1/peliculas/` → películas
- `/api/v1/peliculas/upload` → subida de imágenes
- `/api/v1/peliculas/imagen/{filename}` → obtener imagen
- `/api/v1/generos/` → géneros
- `/api/v1/directores/` → directores

---

## 🖥️ Frontend

### Páginas principales

- `index.html` → catálogo público
- `login.html` → autenticación
- `admin_panel.html` → panel de administración

### Características

- Renderizado dinámico con JavaScript
- Gestión de estado con `localStorage`
- Validación visual y alertas
- Formularios modales con Bootstrap
- Comunicación directa con la API

---

## 🖼️ Gestión de imágenes (detalle técnico)

- El frontend envía imágenes usando `FormData`
- El backend guarda el archivo en el sistema
- Solo se almacena la URL en la base de datos
- Las imágenes se sirven mediante endpoint público

✔️ Más eficiente  
✔️ Escalable  
✔️ Buena práctica real

---

## 🧪 Tests automatizados

El proyecto incluye **tests de backend implementados con pytest** para asegurar la estabilidad y correcto funcionamiento de la API.

### 📂 Ubicación

```
backend/tests/
```

### 🧠 Qué se testea

- 👤 **Usuarios**
  - Creación
  - Lectura
  - Actualización
  - Eliminación

- 🎭 **Géneros**
  - CRUD completo

- 🎬 **Directores**
  - CRUD
  - Operaciones bulk

- 🎥 **Películas**
  - CRUD completo
  - Relaciones con géneros y director
  - Validación de datos

### ▶️ Ejecución de los tests

Desde la carpeta `backend`:

```bash
pytest
```

Los tests están aislados del frontend y permiten validar la lógica de negocio y los endpoints REST.

---

## ⚙️ Configuración del entorno

### Backend (.env)

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=movie_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
```

### Frontend

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
```

---

## ▶️ Ejecución del proyecto

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

Abrir directamente en el navegador:

```
frontend/index.html
```

---

## 🧠 Buenas prácticas aplicadas

- Separación clara frontend / backend
- Arquitectura en capas
- Uso correcto de HTTP verbs
- Validaciones robustas
- Seguridad con JWT
- Código mantenible y escalable

---

## 🚀 Estado del proyecto

✅ Funcional  
✅ Documentado  
✅ Testeado  
✅ Listo para evaluación / portfolio / GitHub

---

## 💡 Próximas mejoras posibles

- Deploy con Docker
- Variables de entorno centralizadas
- Paginación
- Tests de frontend
- UI con framework moderno (React / Vue)
