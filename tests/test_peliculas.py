from fastapi import status

def create_director_helper(client):
    res = client.post("/api/v1/directores/", json={"nombre": "Director Test", "anio_nacimiento": 1970})
    return res.json()["id"]

def create_genero_helper(client):
    res = client.post("/api/v1/generos/", json={"nombre": "Action Test"})
    return res.json()["id"]

def test_create_pelicula(client):
    dir_id = create_director_helper(client)
    gen_id = create_genero_helper(client)
    
    response = client.post(
        "/api/v1/peliculas/",
        json={
            "titulo": "Inception",
            "anio": 2010,
            "descripcion": "Dream within a dream",
            "id_director": dir_id,
            "generos": [gen_id]
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["titulo"] == "Inception"
    assert data["id_director"] == dir_id
    assert "id" in data

def test_read_peliculas(client):
    dir_id = create_director_helper(client)
    client.post("/api/v1/peliculas/", json={"titulo": "P1", "id_director": dir_id})
    client.post("/api/v1/peliculas/", json={"titulo": "P2", "id_director": dir_id})
    
    response = client.get("/api/v1/peliculas/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2

def test_read_pelicula_by_id(client):
    dir_id = create_director_helper(client)
    res_create = client.post("/api/v1/peliculas/", json={"titulo": "Target Movie", "id_director": dir_id})
    pelicula_id = res_create.json()["id"]

    response = client.get(f"/api/v1/peliculas/{pelicula_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["titulo"] == "Target Movie"

def test_update_pelicula(client):
    dir_id = create_director_helper(client)
    res_create = client.post("/api/v1/peliculas/", json={"titulo": "Old Title", "id_director": dir_id})
    pelicula_id = res_create.json()["id"]

    response = client.patch(
        f"/api/v1/peliculas/{pelicula_id}",
        json={"titulo": "New Title"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["titulo"] == "New Title"

def test_delete_pelicula(client):
    dir_id = create_director_helper(client)
    res_create = client.post("/api/v1/peliculas/", json={"titulo": "To Delete", "id_director": dir_id})
    pelicula_id = res_create.json()["id"]

    response = client.delete(f"/api/v1/peliculas/{pelicula_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_get = client.get(f"/api/v1/peliculas/{pelicula_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND # Asumiendo hard delete o filtro activo
