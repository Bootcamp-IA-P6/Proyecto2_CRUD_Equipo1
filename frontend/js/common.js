/**
 * common.js
 * Configuración global, manejo de Token y Roles.
 */

// URL base de tu API (Asegúrate que coincida con tu backend FastAPI)
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; 

// --- HERRAMIENTAS DE TOKEN ---

// 1. Obtener headers con la "llave" para entrar a sitios privados
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` // Aquí va el token
    };
}

// 2. Leer la información dentro del Token (sin librerías externas)
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

// --- GESTIÓN DE LA INTERFAZ (UI) ---

/**
 * Esta función se ejecuta al cargar las páginas.
 * Decide qué botones mostrar según quién eres.
 */
function updateNavbarAuth() {
    const token = localStorage.getItem('access_token');
    const loginLink = document.getElementById('nav-login');
    const logoutLink = document.getElementById('nav-logout');
    const adminLink = document.getElementById('nav-admin'); // El botón clave

    if (token) {
        // Estás logueado
        if(loginLink) loginLink.style.display = 'none';
        if(logoutLink) logoutLink.style.display = 'block';

        // Verificamos si eres ADMIN
        const payload = parseJwt(token);
        
        // NOTA: Asegúrate que tu backend envíe 'role': 'admin' o 'is_superuser': true
        if (payload && (payload.role === 'admin' || payload.is_superuser === true)) {
            if(adminLink) adminLink.style.display = 'block'; // ¡Muestra el botón!
        } else {
            if(adminLink) adminLink.style.display = 'none';  // Oculta el botón a clientes
        }

    } else {
        // Eres un visitante anónimo
        if(loginLink) loginLink.style.display = 'block';
        if(logoutLink) logoutLink.style.display = 'none';
        if(adminLink) adminLink.style.display = 'none';
    }
}

// Cerrar sesión
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = 'index.html';
}