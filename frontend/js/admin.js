// Variable global para manejar el modal de Bootstrap
let movieModal;
let selectedGeneros = []; // ← NUEVO: Array para géneros seleccionados

document.addEventListener('DOMContentLoaded', () => {
    // 1. Verificación de seguridad: ¿Es admin?
    const token = localStorage.getItem('access_token');
    const user = parseJwt(token);

    if (!user || (user.role !== 'admin' && !user.is_superuser)) {
        window.location.href = 'index.html'; // Expulsar si no es admin
        return;
    }

    // 2. Inicializar componentes
    movieModal = new bootstrap.Modal(document.getElementById('movieModal'));
    loadMoviesTable();
    loadGenerosTable();
    loadDirectoresTable();
    loadUsuariosTable();
});

// --- LEER (READ) ---
async function loadMoviesTable() {
    const tbody = document.getElementById('movies-table-body');
    tbody.innerHTML = '<tr><td colspan="7" class="text-center">Cargando datos...</td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/peliculas/`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) throw new Error("Error al cargar");

        const movies = await response.json();
        tbody.innerHTML = '';

        movies.forEach(movie => {
            const fileName = movie.poster_url 
                ? movie.poster_url.split('/').pop()
                : 'Sin imagen';
            
            const directorNombre = movie.director ? movie.director.nombre : 'Sin director';
            
            // ← NUEVO: Extraer nombres de géneros
            const generoNombres = movie.generos && movie.generos.length > 0
                ? movie.generos.map(g => g.nombre).join(', ')
                : 'Sin género';

            const row = `
                <tr>
                    <td>${movie.id}</td>
                    <td>
                        <span class="badge bg-info">${fileName}</span>
                    </td>
                    <td class="fw-bold">${movie.titulo}</td>
                    <td>${directorNombre}</td>
                    <td>${generoNombres}</td>
                    <td>${movie.anio || '-'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary me-1" onclick='openEditMovieModal(${JSON.stringify(movie)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteMovie(${movie.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });

    } catch (error) {
        console.error(error);
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error de conexión</td></tr>';
    }
}

// ============ PELÍCULAS ============

function openCreateMovieModal() {
    document.getElementById('movieForm').reset();
    document.getElementById('movieId').value = '';
    document.getElementById('movieModalTitle').innerText = 'Nueva Película';
    
    selectedGeneros = []; // ← RESET géneros
    document.getElementById('generosSelectedTags').innerHTML = '';
    
    loadDirectoresSelect();
    setupGenerosSearch();
    
    new bootstrap.Modal(document.getElementById('movieModal')).show();
}

function openEditMovieModal(movie) {
    document.getElementById('movieId').value = movie.id;
    document.getElementById('movieTitulo').value = movie.titulo;
    document.getElementById('movieDescripcion').value = movie.descripcion || '';
    document.getElementById('movieAnio').value = movie.anio || '';
    document.getElementById('moviePosterFile').value = '';
    
    document.getElementById('movieModalTitle').innerText = 'Editar Película';
    
    // Establecer géneros seleccionados
    selectedGeneros = movie.generos ? movie.generos.map(g => ({ id: g.id, nombre: g.nombre })) : [];
    updateGenerosTags();
    
    loadDirectoresSelect().then(() => {
        setTimeout(() => {
            document.getElementById('movieDirectorId').value = movie.id_director;
        }, 100);
    });
    
    setupGenerosSearch();
    
    new bootstrap.Modal(document.getElementById('movieModal')).show();
}

// Cargar directores en el select
async function loadDirectoresSelect() {
    const select = document.getElementById('movieDirectorId');
    try {
        const response = await fetch(`${API_BASE_URL}/directores/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Error");
        
        const directores = await response.json();
        select.innerHTML = '<option value="">Seleccionar director...</option>';
        
        directores.forEach(director => {
            const option = document.createElement('option');
            option.value = director.id;
            option.textContent = director.nombre;
            select.appendChild(option);
        });
        
        return true;
    } catch (error) {
        console.error(error);
        return false;
    }
}

// ← NUEVO: Setup para búsqueda de géneros
async function setupGenerosSearch() {
    const searchInput = document.getElementById('generosSearchInput');
    const selectorContainer = document.getElementById('generosSelectorContainer');
    const generosList = document.getElementById('generosList');
    const addNewGeneroBtn = document.getElementById('addNewGeneroBtn');
    
    // Limpiar búsqueda
    searchInput.value = '';
    generosList.innerHTML = '';
    selectorContainer.style.display = 'none';
    
    searchInput.addEventListener('input', async (e) => {
        const query = e.target.value.toLowerCase().trim();
        
        try {
            const response = await fetch(`${API_BASE_URL}/generos/`, {
                headers: getAuthHeaders()
            });
            const todosGeneros = await response.json();
            
            // Filtrar géneros no seleccionados
            const filtrados = todosGeneros.filter(g => 
                g.nombre.toLowerCase().includes(query) &&
                !selectedGeneros.some(sg => sg.id === g.id)
            );
            
            generosList.innerHTML = '';
            
            if (filtrados.length > 0) {
                filtrados.forEach(genero => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'btn btn-sm btn-outline-primary me-2 mb-2';
                    btn.textContent = genero.nombre;
                    btn.addEventListener('click', () => {
                        selectedGeneros.push({ id: genero.id, nombre: genero.nombre });
                        updateGenerosTags();
                        setupGenerosSearch();
                    });
                    generosList.appendChild(btn);
                });
            }
            
            // Mostrar opción de crear nuevo si hay búsqueda y no hay resultados
            if (query && filtrados.length === 0) {
                addNewGeneroBtn.style.display = 'block';
                addNewGeneroBtn.textContent = `➕ Crear "${query}"`;
                addNewGeneroBtn.onclick = async () => {
                    await createAndAddGenero(query);
                };
            } else {
                addNewGeneroBtn.style.display = 'none';
            }
            
            selectorContainer.style.display = 'block';
        } catch (error) {
            console.error(error);
        }
    });
}

// ← NUEVO: Crear nuevo género y agregarlo
async function createAndAddGenero(nombre) {
    try {
        const response = await fetch(`${API_BASE_URL}/generos/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ nombre: nombre })
        });
        
        if (response.ok) {
            const nuevoGenero = await response.json();
            selectedGeneros.push({ id: nuevoGenero.id, nombre: nuevoGenero.nombre });
            updateGenerosTags();
            setupGenerosSearch();
            Swal.fire('Éxito', `Género "${nombre}" creado`, 'success');
        }
    } catch (error) {
        Swal.fire('Error', 'No se pudo crear el género', 'error');
    }
}

// ← NUEVO: Actualizar tags de géneros seleccionados
function updateGenerosTags() {
    const container = document.getElementById('generosSelectedTags');
    container.innerHTML = '';
    
    selectedGeneros.forEach(genero => {
        const tag = document.createElement('span');
        tag.className = 'badge bg-primary';
        tag.style.padding = '8px 12px';
        tag.innerHTML = `
            ${genero.nombre}
            <button type="button" class="btn-close btn-close-white ms-2" 
                    onclick="removeGenero(${genero.id})" 
                    style="padding: 0; margin: 0; font-size: 0.8rem;">
            </button>
        `;
        container.appendChild(tag);
    });
}

// ← NUEVO: Remover género de selección
function removeGenero(generoId) {
    selectedGeneros = selectedGeneros.filter(g => g.id !== generoId);
    updateGenerosTags();
    setupGenerosSearch();
}

async function saveMovie() {
    const id = document.getElementById('movieId').value;
    const posterFile = document.getElementById('moviePosterFile').files[0];
    
    let posterUrl = null;
    
    // Si hay archivo, subirlo PRIMERO
    if (posterFile) {
        console.log("Subiendo archivo:", posterFile.name);
        
        const formData = new FormData();
        formData.append('file', posterFile);
        
        try {
            const uploadResponse = await fetch(`${API_BASE_URL}/peliculas/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    // NO incluir Content-Type, fetch lo hace automáticamente
                },
                body: formData
            });
            
            console.log("Respuesta upload:", uploadResponse.status);
            
            if (!uploadResponse.ok) {
                const errorData = await uploadResponse.json();
                console.error("Error del servidor:", errorData);
                Swal.fire('Error en imagen', errorData.detail || 'Error desconocido', 'error');
                return; // No continuar si falla la imagen
            }
            
            const uploadResult = await uploadResponse.json();
            posterUrl = uploadResult.poster_url;
            console.log("Imagen subida correctamente:", posterUrl);
            
        } catch (error) {
            console.error("Error subiendo imagen:", error);
            Swal.fire('Error de conexión', 'No se pudo subir la imagen. Verifica la consola.', 'error');
            return;
        }
    }
    
    // Recolectar datos del form
    const data = {
        titulo: document.getElementById('movieTitulo').value,
        descripcion: document.getElementById('movieDescripcion').value,
        anio: parseInt(document.getElementById('movieAnio').value) || null,
        id_director: parseInt(document.getElementById('movieDirectorId').value),
        generos: selectedGeneros.map(g => g.id),
        poster_url: posterUrl // Puede ser null si no hay imagen
    };

    console.log("Datos a enviar:", data);

    const method = id ? 'PATCH' : 'POST';
    const url = id ? `${API_BASE_URL}/peliculas/${id}` : `${API_BASE_URL}/peliculas/`;

    try {
        const response = await fetch(url, {
            method: method,
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });

        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('movieModal')).hide();
            Swal.fire({
                icon: 'success',
                title: 'Guardado',
                text: 'La película se guardó correctamente',
                timer: 1500,
                showConfirmButton: false
            });
            loadMoviesTable();
        } else {
            const err = await response.json();
            console.error("Error al guardar película:", err);
            Swal.fire('Error', err.detail || 'Algo salió mal', 'error');
        }
    } catch (error) {
        console.error("Error:", error);
        Swal.fire('Error', 'No se pudo conectar con el servidor', 'error');
    }
}

async function deleteMovie(id) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "No podrás revertir esto.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`${API_BASE_URL}/peliculas/${id}`, {
                    method: 'DELETE',
                    headers: getAuthHeaders()
                });

                if (response.ok) {
                    Swal.fire('¡Eliminado!', 'La película ha sido eliminada.', 'success');
                    loadMoviesTable();
                } else {
                    Swal.fire('Error', 'No se pudo eliminar.', 'error');
                }
            } catch (error) {
                Swal.fire('Error', 'Error de red.', 'error');
            }
        }
    });
}

// ============ GÉNEROS ============
async function loadGenerosTable() {
    const tbody = document.getElementById('generos-table-body');
    try {
        const response = await fetch(`${API_BASE_URL}/generos/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Error al cargar géneros");
        
        const generos = await response.json();
        tbody.innerHTML = '';
        
        generos.forEach(genero => {
            const row = `
                <tr>
                    <td>${genero.id}</td>
                    <td>${genero.nombre}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary me-1" onclick='openEditGeneroModal(${JSON.stringify(genero)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteGenero(${genero.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error(error);
        tbody.innerHTML = '<tr><td colspan="3" class="text-center text-danger">Error de conexión</td></tr>';
    }
}

function openCreateGeneroModal() {
    document.getElementById('generoForm').reset();
    document.getElementById('generoId').value = '';
    document.getElementById('generoModalTitle').innerText = 'Nuevo Género';
    new bootstrap.Modal(document.getElementById('generoModal')).show();
}

function openEditGeneroModal(genero) {
    document.getElementById('generoId').value = genero.id;
    document.getElementById('generoNombre').value = genero.nombre;
    document.getElementById('generoModalTitle').innerText = 'Editar Género';
    new bootstrap.Modal(document.getElementById('generoModal')).show();
}

async function saveGenero() {
    const id = document.getElementById('generoId').value;
    const data = { nombre: document.getElementById('generoNombre').value };
    
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE_URL}/generos/${id}` : `${API_BASE_URL}/generos/`;
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            Swal.fire('Éxito', 'Género guardado', 'success');
            loadGenerosTable();
            bootstrap.Modal.getInstance(document.getElementById('generoModal')).hide();
        } else {
            Swal.fire('Error', 'No se pudo guardar', 'error');
        }
    } catch (error) {
        Swal.fire('Error', 'Error de conexión', 'error');
    }
}

async function deleteGenero(id) {
    Swal.fire({
        title: '¿Eliminar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`${API_BASE_URL}/generos/${id}`, {
                    method: 'DELETE',
                    headers: getAuthHeaders()
                });
                if (response.ok) {
                    Swal.fire('¡Eliminado!', 'Género eliminado', 'success');
                    loadGenerosTable();
                }
            } catch (error) {
                Swal.fire('Error', 'Error al eliminar', 'error');
            }
        }
    });
}

// ============ DIRECTORES ============
async function loadDirectoresTable() {
    const tbody = document.getElementById('directores-table-body');
    try {
        const response = await fetch(`${API_BASE_URL}/directores/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Error");
        
        const directores = await response.json();
        tbody.innerHTML = '';
        
        directores.forEach(director => {
            const row = `
                <tr>
                    <td>${director.id}</td>
                    <td>${director.nombre}</td>
                    <td>${director.anio_nacimiento || '-'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary me-1" onclick='openEditDirectorModal(${JSON.stringify(director)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteDirector(${director.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error</td></tr>';
    }
}

function openCreateDirectorModal() {
    document.getElementById('directorForm').reset();
    document.getElementById('directorId').value = '';
    document.getElementById('directorModalTitle').innerText = 'Nuevo Director';
    new bootstrap.Modal(document.getElementById('directorModal')).show();
}

function openEditDirectorModal(director) {
    document.getElementById('directorId').value = director.id;
    document.getElementById('directorNombre').value = director.nombre;
    document.getElementById('directorAnio').value = director.anio_nacimiento || '';
    document.getElementById('directorModalTitle').innerText = 'Editar Director';
    new bootstrap.Modal(document.getElementById('directorModal')).show();
}

async function saveDirector() {
    const id = document.getElementById('directorId').value;
    const data = {
        nombre: document.getElementById('directorNombre').value,
        anio_nacimiento: parseInt(document.getElementById('directorAnio').value) || null
    };
    
    const method = id ? 'PATCH' : 'POST';
    const url = id ? `${API_BASE_URL}/directores/${id}` : `${API_BASE_URL}/directores/`;
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            Swal.fire('Éxito', 'Director guardado', 'success');
            loadDirectoresTable();
            bootstrap.Modal.getInstance(document.getElementById('directorModal')).hide();
        } else {
            Swal.fire('Error', 'No se pudo guardar', 'error');
        }
    } catch (error) {
        Swal.fire('Error', 'Error de conexión', 'error');
    }
}

async function deleteDirector(id) {
    Swal.fire({
        title: '¿Eliminar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`${API_BASE_URL}/directores/${id}`, {
                    method: 'DELETE',
                    headers: getAuthHeaders()
                });
                if (response.ok) {
                    Swal.fire('¡Eliminado!', '', 'success');
                    loadDirectoresTable();
                }
            } catch (error) {
                Swal.fire('Error', 'Error al eliminar', 'error');
            }
        }
    });
}

// ============ USUARIOS ============
async function loadUsuariosTable() {
    const tbody = document.getElementById('usuarios-table-body');
    try {
        const response = await fetch(`${API_BASE_URL}/users/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Error");
        
        const usuarios = await response.json();
        tbody.innerHTML = '';
        
        usuarios.forEach(user => {
            const row = `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td><span class="badge ${user.role === 'admin' ? 'bg-danger' : 'bg-info'}">${user.role}</span></td>
                    <td>${user.is_active ? '<span class="badge bg-success">Activo</span>' : '<span class="badge bg-secondary">Inactivo</span>'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary me-1" onclick='openEditUserModal(${JSON.stringify(user)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error</td></tr>';
    }
}

function openEditUserModal(user) {
    document.getElementById('userId').value = user.id;
    document.getElementById('userName').value = user.username;
    document.getElementById('userEmail').value = user.email;
    document.getElementById('userRole').value = user.role;
    document.getElementById('userActive').checked = user.is_active;
    document.getElementById('userModalTitle').innerText = 'Editar Usuario';
    new bootstrap.Modal(document.getElementById('userModal')).show();
}

async function saveUser() {
    const id = document.getElementById('userId').value;
    const data = {
        username: document.getElementById('userName').value,
        email: document.getElementById('userEmail').value,
        role: document.getElementById('userRole').value,
        is_active: document.getElementById('userActive').checked
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/${id}`, {
            method: 'PATCH',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            Swal.fire('Éxito', 'Usuario actualizado', 'success');
            loadUsuariosTable();
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
        } else {
            Swal.fire('Error', 'No se pudo actualizar', 'error');
        }
    } catch (error) {
        Swal.fire('Error', 'Error de conexión', 'error');
    }
}