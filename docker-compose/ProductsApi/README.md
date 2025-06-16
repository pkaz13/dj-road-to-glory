# Products API

A .NET 8 Web API for managing products and categories, featuring SQL Server for persistent storage and Redis for caching. The project is containerized using Docker Compose for easy local development and deployment.

---

## ⚠️ Important: Set the SQL Server Password

Before running the project, you **must** set a secure password for the SQL Server. The placeholder `__sqlPassword__` is used in several files and must be replaced with your chosen password **everywhere it appears**.

### Files to Update:

- `src/ProductsApi/appsettings.json`
- `src/ProductsApi/appsettings.Development.json`
- `secrets/db_password.txt`

Replace all instances of `__sqlPassword__` with your actual password. For example:

```
"DefaultConnection": "Server=sqlserver;Database=ProductsDb;User Id=sa;Password=YourStrongPassword!;TrustServerCertificate=True;"
```

And in `secrets/db_password.txt`, the file should contain only your password (no quotes, no spaces).

---

## 🚀 Running the Project with Docker Compose

### 1. Build and Start All Services

From the root directory, run:

```
docker compose up --build -d
```

This will:
- Build the API Docker image
- Start the API, SQL Server, and Redis containers
- Apply database migrations automatically on first run

The API will be available at: [http://localhost:5050](http://localhost:5050)

### 2. Stopping the Services

To stop all running containers (without removing data):

```
docker compose down
```

### 3. Cleaning Up (Remove Volumes and Networks)

To remove all containers, networks, and **persistent data** (SQL/Redis):

```
docker compose down -v
```

> **Warning:** This will delete all data stored in SQL Server and Redis.

---

## 🛠️ Additional Notes

- **Database Migrations:**
  - Migrations are applied automatically on startup if the database is missing or out of date.
  - Migration files are located in `src/ProductsApi/Migrations/`.
- **Secrets:**
  - The SQL Server password is managed via Docker secrets (`secrets/db_password.txt`).
- **Environment Switching:**
  - The API uses `appsettings.json` for production and `appsettings.Development.json` for development. Adjust connection strings as needed.
- **Swagger UI:**
  - In development mode, Swagger UI is available at `/swagger`.
- **Ports:**
  - API: `localhost:5050`
  - SQL Server: `localhost:1433`
  - Redis: `localhost:6379`

---

## 📂 Project Structure

- `docker-compose.yml` - Docker Compose configuration
- `src/` - Source code and Dockerfile
- `secrets/` - SQL Server password secret

---

## ❓ Troubleshooting

- Ensure you have Docker and Docker Compose installed.
- Make sure to set a strong SQL Server password (meets SQL Server requirements).
- If you change the password, update it in **all** locations listed above.
- If you encounter database connection issues, check that the password is correct and all services are healthy.

---

Enjoy developing with Products API! 