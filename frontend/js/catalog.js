const MAX_IMAGE_RETRIES = 3;

async function loadMovies() {
    const grid = document.getElementById('movies-grid');
    
    try {
        const response = await fetch(`${API_BASE_URL}/peliculas/`);
        
        if (!response.ok) throw new Error("Error al cargar películas");
        
        const movies = await response.json();
        
        if (movies.length === 0) {
            grid.innerHTML = '<div class="text-center w-100"><p class="text-secondary">No hay películas disponibles</p></div>';
            return;
        }
        
        grid.innerHTML = '';
        
        movies.forEach(movie => {
            // ← CRÍTICO: Construir URL correctamente
            let posterUrl = null;
            if (movie.poster_url) {
                // Si empieza con /, es ruta de API
                if (movie.poster_url.startsWith('/')) {
                    posterUrl = `http://localhost:8000${movie.poster_url}`;
                } else {
                    posterUrl = `http://localhost:8000${movie.poster_url}`;
                }
            }
            
            const placeholderSvg = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='450'%3E%3Crect fill='%23333' width='300' height='450'/%3E%3Ctext x='50%25' y='50%25' font-size='18' fill='%23fff' text-anchor='middle' dy='.3em'%3ESin Imagen%3C/text%3E%3C/svg%3E`;
            
            const card = `
                <div class="col">
                    <div class="card movie-card h-100">
                        <img src="${posterUrl || placeholderSvg}" 
                             class="card-img-top" 
                             alt="${movie.titulo}"
                             data-retries="0"
                             onerror="handleImageError(this, '${placeholderSvg}')">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${movie.titulo}</h5>
                            <p class="card-text text-secondary text-truncate">${movie.descripcion || 'Sin descripción'}</p>
                            <p class="text-sm text-muted">${movie.anio || 'Año desconocido'}</p>
                            <button class="btn btn-custom-red mt-auto" onclick='openMovieDetail(${JSON.stringify(movie)})'>
                                <i class="fas fa-play"></i> Ver
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            grid.innerHTML += card;
        });
        
    } catch (error) {
        console.error("Error:", error);
        grid.innerHTML = '<div class="text-center w-100 text-danger"><p>Error al cargar las películas</p></div>';
    }
}

function handleImageError(img, placeholder) {
    let retries = parseInt(img.getAttribute('data-retries') || '0');
    
    if (retries < MAX_IMAGE_RETRIES) {
        retries++;
        img.setAttribute('data-retries', retries);
        setTimeout(() => {
            img.src = img.src;
        }, 500);
    } else {
        img.src = placeholder;
        img.style.opacity = '0.7';
    }
}

function openMovieDetail(movie) {
    console.log("Abriendo película:", movie);
    alert(`${movie.titulo} - ${movie.anio}`);
}

document.addEventListener('DOMContentLoaded', () => {
    loadMovies();
    checkUserStatus();
});