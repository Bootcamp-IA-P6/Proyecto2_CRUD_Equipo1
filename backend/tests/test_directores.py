from fastapi import status

def test_create_director(client):
    response = client.post(
        "/api/v1/directores/",
        json={"nombre": "Christopher Nolan", "anio_nacimiento": 1970}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre"] == "Christopher Nolan"
    assert "id" in data

def test_read_directores(client):
    client.post("/api/v1/directores/", json={"nombre": "D1", "anio_nacimiento": 1980})
    client.post("/api/v1/directores/", json={"nombre": "D2", "anio_nacimiento": 1990})
    
    response = client.get("/api/v1/directores/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2

def test_read_director_by_id(client):
    res_create = client.post("/api/v1/directores/", json={"nombre": "Target Director", "anio_nacimiento": 1980})
    director_id = res_create.json()["id"]

    response = client.get(f"/api/v1/directores/{director_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nombre"] == "Target Director"

def test_update_director(client):
    res_create = client.post("/api/v1/directores/", json={"nombre": "Old Name", "anio_nacimiento": 1950})
    director_id = res_create.json()["id"]

    response = client.patch(
        f"/api/v1/directores/{director_id}",
        json={"nombre": "New Name"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nombre"] == "New Name"
    assert response.json()["anio_nacimiento"] == 1950

def test_delete_director(client):
    res_create = client.post("/api/v1/directores/", json={"nombre": "To Delete", "anio_nacimiento": 1900})
    director_id = res_create.json()["id"]

    response = client.delete(f"/api/v1/directores/{director_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que ya no existe
    # Asumiendo que GET devuelve 404 si no existe (no soft delete mencionado en director)
    response_get = client.get(f"/api/v1/directores/{director_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND
