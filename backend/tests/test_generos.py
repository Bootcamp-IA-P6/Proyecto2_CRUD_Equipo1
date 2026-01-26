from fastapi import status

def test_create_genero(client):
    response = client.post(
        "/api/v1/generos/",
        json={"nombre": "Acción"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre"] == "Acción"
    assert "id" in data

def test_read_generos(client):
    client.post("/api/v1/generos/", json={"nombre": "Drama"})
    client.post("/api/v1/generos/", json={"nombre": "Comedia"})
    
    response = client.get("/api/v1/generos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2

def test_read_genero_by_id(client):
    res_create = client.post("/api/v1/generos/", json={"nombre": "Terror"})
    genero_id = res_create.json()["id"]

    response = client.get(f"/api/v1/generos/{genero_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nombre"] == "Terror"

def test_update_genero(client):
    res_create = client.post("/api/v1/generos/", json={"nombre": "Old Genero"})
    genero_id = res_create.json()["id"]

    # PUT o PATCH? Routes dice PUT y DELETE.
    # @router.put("/{genero_id}", response_model=GeneroResponse)
    response = client.put(
        f"/api/v1/generos/{genero_id}",
        json={"nombre": "New Genero"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nombre"] == "New Genero"

def test_delete_genero(client):
    res_create = client.post("/api/v1/generos/", json={"nombre": "To Delete"})
    genero_id = res_create.json()["id"]

    response = client.delete(f"/api/v1/generos/{genero_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_get = client.get(f"/api/v1/generos/{genero_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND
