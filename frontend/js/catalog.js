document.addEventListener('DOMContentLoaded', () => {
    updateNavbarAuth(); // Verificar rol al cargar
    loadMovies();
});

async function loadMovies() {
    const grid = document.getElementById('movies-grid');
    
    try {
        // Petición GET al endpoint público (o protegido según tu API)
        const response = await fetch(`${API_BASE_URL}/peliculas/`); // Endpoint basado en tu imagen
        
        if (!response.ok) throw new Error('Error al cargar películas');
        
        const movies = await response.json();
        
        grid.innerHTML = ''; // Limpiar spinner

        if (movies.length === 0) {
            grid.innerHTML = '<p class="text-center text-white">No hay películas disponibles.</p>';
            return;
        }

        // Generar HTML por cada película
        movies.forEach(movie => {
            const card = `
                <div class="col">
                    <div class="card movie-card">
                        <img src="${movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image'}" class="card-img-top" alt="${movie.titulo}">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${movie.titulo}</h5>
                            <p class="card-text text-secondary small flex-grow-1">${movie.descripcion ? movie.descripcion.substring(0, 80) + '...' : 'Sin descripción'}</p>
                            <div class="mt-2 d-flex justify-content-between align-items-center">
                                <span class="badge badge-genre">Género ID: ${movie.genero_id}</span> <!-- Podrías mapear ID a nombre -->
                            </div>
                        </div>
                    </div>
                </div>
            `;
            grid.innerHTML += card;
        });

    } catch (error) {
        console.error(error);
        grid.innerHTML = `<div class="alert alert-danger w-100">Error cargando el catálogo. Asegúrate de que el backend está corriendo.</div>`;
    }
}