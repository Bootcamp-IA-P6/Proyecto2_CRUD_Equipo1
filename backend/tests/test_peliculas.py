from fastapi import status

def create_admin_user(client):
    res = client.post("/api/v1/users/", json={
        "username": "admin_test",
        "email": "admin@test.com",
        "password": "password123",
        "role": "admin"
    })
    return res.json()

def get_admin_token(client):
    create_admin_user(client)
    res = client.post("/token", data={
        "username": "admin_test",
        "password": "password123"
    })
    return res.json()["access_token"]

def create_director_helper(client):
    res = client.post("/api/v1/directores/", json={"nombre": "Director Test", "anio_nacimiento": 1970})
    return res.json()["id"]

def create_genero_helper(client):
    res = client.post("/api/v1/generos/", json={"nombre": "Action Test"})
    return res.json()["id"]

def test_create_pelicula(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
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
        },
        headers=headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["titulo"] == "Inception"
    assert data["id_director"] == dir_id
    assert "id" in data

def test_read_peliculas(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    dir_id = create_director_helper(client)
    client.post("/api/v1/peliculas/", json={"titulo": "P1", "id_director": dir_id}, headers=headers)
    client.post("/api/v1/peliculas/", json={"titulo": "P2", "id_director": dir_id}, headers=headers)
    
    response = client.get("/api/v1/peliculas/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2

def test_read_pelicula_by_id(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    dir_id = create_director_helper(client)
    res_create = client.post("/api/v1/peliculas/", json={"titulo": "Target Movie", "id_director": dir_id}, headers=headers)
    pelicula_id = res_create.json()["id"]

    response = client.get(f"/api/v1/peliculas/{pelicula_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["titulo"] == "Target Movie"

def test_update_pelicula(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    dir_id = create_director_helper(client)
    res_create = client.post("/api/v1/peliculas/", json={"titulo": "Old Title", "id_director": dir_id}, headers=headers)
    pelicula_id = res_create.json()["id"]

    response = client.patch(
        f"/api/v1/peliculas/{pelicula_id}",
        json={"titulo": "New Title"},
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["titulo"] == "New Title"

def test_delete_pelicula(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    dir_id = create_director_helper(client)
    res_create = client.post("/api/v1/peliculas/", json={"titulo": "To Delete", "id_director": dir_id}, headers=headers)
    pelicula_id = res_create.json()["id"]

    response = client.delete(f"/api/v1/peliculas/{pelicula_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    response_get = client.get(f"/api/v1/peliculas/{pelicula_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND
