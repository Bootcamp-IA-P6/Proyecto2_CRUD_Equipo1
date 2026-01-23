// Variable global para manejar el modal de Bootstrap
let movieModal;

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
});

// --- LEER (READ) ---
async function loadMoviesTable() {
    const tbody = document.getElementById('movies-table-body');
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Cargando datos...</td></tr>';

    try {
        // Petición GET al backend
        const response = await fetch(`${API_BASE_URL}/peliculas/`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) throw new Error("Error al cargar");

        const movies = await response.json();
        tbody.innerHTML = ''; // Limpiar tabla

        movies.forEach(movie => {
            // Renderizamos la fila
            const row = `
                <tr>
                    <td>${movie.id}</td>
                    <td>
                        <img src="${movie.poster_url || 'https://via.placeholder.com/50'}" 
                             alt="poster" style="width: 40px; height: 60px; object-fit: cover; border-radius: 4px;">
                    </td>
                    <td class="fw-bold">${movie.titulo}</td>
                    <td><span class="badge bg-secondary">ID: ${movie.genero_id}</span></td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary me-1" onclick='openEditModal(${JSON.stringify(movie)})'>
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
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error de conexión</td></tr>';
    }
}

// --- PREPARAR MODAL ---

function openCreateModal() {
    // Limpiamos el formulario para crear algo nuevo
    document.getElementById('movieForm').reset();
    document.getElementById('movieId').value = ''; // ID vacío = CREAR
    document.getElementById('modalTitle').innerText = 'Nueva Película';
    movieModal.show();
}

function openEditModal(movie) {
    // Rellenamos el formulario con los datos existentes
    document.getElementById('movieId').value = movie.id;
    document.getElementById('movieTitulo').value = movie.titulo;
    document.getElementById('movieDescripcion').value = movie.descripcion;
    document.getElementById('movieGeneroId').value = movie.genero_id;
    document.getElementById('moviePoster').value = movie.poster_url;
    
    document.getElementById('modalTitle').innerText = 'Editar Película';
    movieModal.show();
}

// --- CREAR Y ACTUALIZAR (CREATE / UPDATE) ---
async function saveMovie() {
    const id = document.getElementById('movieId').value;
    
    // Recolectar datos del form
    const data = {
        titulo: document.getElementById('movieTitulo').value,
        descripcion: document.getElementById('movieDescripcion').value,
        genero_id: parseInt(document.getElementById('movieGeneroId').value),
        poster_url: document.getElementById('moviePoster').value
    };

    // Decidir si es POST (Crear) o PATCH (Actualizar)
    const method = id ? 'PATCH' : 'POST';
    const url = id ? `${API_BASE_URL}/peliculas/${id}` : `${API_BASE_URL}/peliculas/`;

    try {
        const response = await fetch(url, {
            method: method,
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });

        if (response.ok) {
            movieModal.hide();
            Swal.fire({
                icon: 'success',
                title: 'Guardado',
                text: 'La operación se realizó con éxito',
                timer: 1500,
                showConfirmButton: false
            });
            loadMoviesTable(); // Recargar la tabla automáticamente
        } else {
            const err = await response.json();
            Swal.fire('Error', err.detail || 'Algo salió mal', 'error');
        }
    } catch (error) {
        Swal.fire('Error', 'No se pudo conectar con el servidor', 'error');
    }
}

// --- ELIMINAR (DELETE) ---
function deleteMovie(id) {
    // Usamos SweetAlert2 para una confirmación bonita
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