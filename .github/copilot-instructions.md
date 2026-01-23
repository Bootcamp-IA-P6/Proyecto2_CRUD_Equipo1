# Copilot Instructions for Proyecto2_CRUD_Equipo1

## Architecture Overview
This is a FastAPI-based CRUD API for a movie catalog system using SQLAlchemy ORM with MySQL database. The application manages movies, directors, genres, and users with role-based access.

- **Project Structure**: Organized in `src/` with:
  - `models/`: SQLAlchemy ORM models (e.g., `Pelicula`, `Director`, `Genero`, `User`)
  - `schemas/`: Pydantic validation schemas (e.g., `PeliculaCreate`, `PeliculaUpdate`)
  - `controllers/`: Business logic functions (CRUD operations)
  - `routes/`: FastAPI route definitions with dependency injection
  - `database/`: DB connection and session management
  - `config/`: Environment-based settings using Pydantic
  - `utils/`: Helper functions (e.g., password hashing with bcrypt)

- **Data Flow**: HTTP requests → Routes (with `Depends(get_db)`) → Controllers → Models/Schemas → MySQL DB
- **Relationships**: Movies link to one director (FK) and multiple genres (many-to-many via `peliculas_genero` junction table)
- **Entry Point**: `main.py` creates tables and includes routers under `/api/v1` prefix

## Key Patterns & Conventions
- **CRUD Operations**: Controllers follow create/get_one/get_all/update(PATCH)/delete pattern. Raise `HTTPException(404)` for missing entities.
- **Updates**: Use `pelicula_update.model_dump(exclude_unset=True)` for partial updates. Handle FKs/relationships separately: query existence, then `setattr` or assign lists (e.g., `db_pelicula.generos = db_generos`).
- **Many-to-Many Handling**: For genres, query `Genero` by IDs, verify all exist (len match), then `new_pelicula.generos.extend(db_generos)` on create or assign on update.
- **Validation**: Pydantic `Field` with min/max lengths, optional fields in updates.
- **DB Sessions**: Yield-based `get_db()` for automatic cleanup.
- **Security**: Passwords hashed via `utils/security.py` using bcrypt.
- **Naming**: Entity names in Spanish (Pelicula), code in English. Import all models in `main.py` for `create_all()`.

## Developer Workflows
- **Run Locally**: `uvicorn main:app --reload` (requires `.env` with DB_USER, DB_PASSWORD, etc.)
- **DB Setup**: Tables auto-created on startup; no migrations.
- **Dependencies**: `pip install -r requirements.txt` in virtual env.
- **Testing**: No explicit test framework; validate via API endpoints.

## Common Pitfalls
- Ensure all routes are imported/included in `main.py` (e.g., `peliculas_routes` is defined but not included).
- Bulk operations (if implemented) must handle transactions properly.
- FK constraints: Always check related entity existence before assignment.</content>
<parameter name="filePath">c:\Users\Coder\Proyectos\Proyecto2_CRUD_Equipo1\.github\copilot-instructions.md