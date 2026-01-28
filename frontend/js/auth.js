/**
 * auth.js
 * Maneja la animación del slider y la lógica de autenticación.
 */

const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

// --- 1. LÓGICA VISUAL (SLIDER) ---
if (signUpButton && signInButton && container) {
    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });
}

// --- 2. LÓGICA DE LOGIN ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('loginUser').value;
        const password = document.getElementById('loginPass').value;
        const msgBox = document.getElementById('login-message');

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            // Ajusta la URL si es necesario
            const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                
                // Decodificar JWT para ver rol
                const payload = parseJwt(data.access_token);
                
                // Redirección basada en Rol
                if (payload.role === 'admin' || payload.is_superuser === true) {
                    window.location.href = 'admin_panel.html';
                } else {
                    window.location.href = 'index.html';
                }
            } else {
                msgBox.innerText = 'Usuario o contraseña incorrectos';
                msgBox.style.display = 'block';
            }
        } catch (error) {
            console.error(error);
            msgBox.innerText = 'Error de conexión';
            msgBox.style.display = 'block';
        }
    });
}

// --- 3. LÓGICA DE REGISTRO ---
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userPayload = {
            username: document.getElementById('regUsername').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value,
            role: "cliente" // Forzamos rol cliente
        };

        const msgBox = document.getElementById('reg-message');

        try {
            const response = await fetch(`${API_BASE_URL}/users/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userPayload)
            });

            if (response.ok) {
                // Éxito: Movemos el slider hacia el login
                alert('¡Registro exitoso! Por favor inicia sesión.');
                container.classList.remove("right-panel-active"); // Desliza al login
                registerForm.reset();
            } else {
                const err = await response.json();
                msgBox.innerText = err.detail || 'Error al registrar';
                msgBox.style.display = 'block';
            }
        } catch (error) {
            msgBox.innerText = 'Error de servidor';
            msgBox.style.display = 'block';
        }
    });
}