# Proyecto2_CRUD_Equipo1

## Instalación

1.  **(Opcional) Crear un entorno virtual**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Mac/Linux
    # venv\Scripts\activate  # En Windows
    ```

2.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
    > Nota: Esto instalará también `bcrypt` y `pytest` necesarios para la aplicación y los tests.

## Configuración

1.  Copiar el archivo de ejemplo de variables de entorno:
    ```bash
    cp .env.example .env
    ```
2.  Editar el archivo `.env` con las credenciales de tu base de datos MySQL (DB_USER, DB_PASSWORD, etc.).

## Ejecución

Para levantar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

La documentación interactiva (Swagger UI) estará disponible en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Testing

El proyecto incluye tests unitarios para los endpoints de Usuarios, Películas, Directores y Géneros.

Para ejecutar todos los tests:

```bash
python3 -m pytest -v
```