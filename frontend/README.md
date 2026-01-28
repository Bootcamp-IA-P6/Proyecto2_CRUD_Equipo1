# 🎬 Movie Catalog – Frontend

Frontend web application for a movie catalog system with authentication and admin management.

Este repositorio contiene el frontend de una aplicación de catálogo de películas que consume una API REST desarrollada en FastAPI.  
La interfaz permite visualizar películas, autenticarse y gestionar recursos desde un panel de administración según el rol del usuario.

---

## ✨ Features

- 📽️ Visualización pública del catálogo de películas
- 🔐 Autenticación basada en JWT
- 👤 Control de acceso por roles (admin / cliente)
- 🛠️ Panel de administración con operaciones CRUD
- 🖼️ Subida de imágenes desde el navegador
- ⚡ Renderizado dinámico con JavaScript puro

---

## 🧑‍💻 Tecnologías utilizadas

- HTML5
- CSS3
- JavaScript (Vanilla JS)
- DOM API
- Fetch API
- JWT (JSON Web Tokens)
- FormData para subida de archivos

🚫 **No se utilizan frameworks ni librerías externas** (React, Vue, Axios, etc.).

---

## 📁 Estructura del proyecto

```
frontend/
├── css/
│   └── styles.css
├── js/
│   ├── admin.js
│   ├── auth.js
│   ├── catalogo.js
│   └── common.js
├── html/
│   ├── admin_panel.html
│   ├── index.html
│   └── login.html
└── .env
```

---

## 📄 Vistas HTML

### index.html

- Página pública del catálogo
- Renderiza las películas obtenidas desde la API
- Accesible sin autenticación

### login.html

- Pantalla de inicio de sesión
- Autenticación mediante usuario y contraseña
- Obtención y almacenamiento del token JWT

### admin_panel.html

- Acceso exclusivo para usuarios con rol admin
- Gestión completa de películas, directores y géneros
- Operaciones CRUD desde la interfaz

---

## 📜 Lógica JavaScript

### common.js

- Funciones compartidas en toda la aplicación
- Gestión del token JWT (localStorage)
- Helpers para peticiones autenticadas
- Control de permisos y sesión

### auth.js

- Lógica de autenticación
- Envío de credenciales al backend
- Manejo de login y logout
- Redirección según rol del usuario

### catalogo.js

- Consumo de endpoints públicos
- Renderizado dinámico del catálogo
- Manipulación directa del DOM

### admin.js

- Funcionalidad del panel de administración
- Gestión de formularios
- Envío de datos al backend
- Subida de imágenes usando FormData

---

## 🔐 Autenticación y seguridad

- Autenticación basada en JWT
- El token se almacena en `localStorage`
- Las peticiones protegidas incluyen el header:

```
Authorization: Bearer <token>
```

- El acceso a vistas administrativas está restringido por rol

---

## 🖼️ Gestión de imágenes

La subida de imágenes se realiza con JavaScript nativo:

- `<input type="file">`
- `FormData`
- `fetch()`

El backend se encarga del almacenamiento y devuelve la URL asociada al recurso.

---

## ▶️ Ejecución del proyecto

El frontend puede ejecutarse de dos formas:

### Opción 1: Directamente en el navegador

Abrir `index.html` con doble clic

### Opción 2: Servidor local (recomendado)

```bash
# Con Live Server (VS Code extension)
# o
# Con http-server
npx http-server
```

⚠️ **El backend debe estar en ejecución para que la aplicación funcione correctamente.**

---

## ⚙️ Variables de entorno

El archivo `.env` contiene la URL base del backend y otras configuraciones necesarias para las peticiones HTTP.

---

## 📌 Requisitos

- Backend activo y accesible
- Navegador moderno compatible con ES6+
- Conexión a internet (si el backend no es local)

---

## 🧠 Notas finales

Este frontend ha sido diseñado con un enfoque en:

- Simplicidad
- Claridad
- Separación de responsabilidades
- Aprendizaje del funcionamiento interno del DOM y Fetch API

**Ideal para proyectos académicos y demostraciones de CRUD completo con autenticación y roles.**
