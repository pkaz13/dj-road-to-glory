# Contracts Automation

This project automates the generation and distribution of API contracts using NSwag, streamlining integration between a .NET API server and a TypeScript web client. The solution ensures that both backend and frontend always use up-to-date, strongly-typed API clients generated from a single OpenAPI specification.

## Project Structure

- **api-server**: .NET API server project. Hosts the backend logic. For simplification, the database is an in-memory List.
- **contracts-nswag**: Contains NSwag configuration and scripts for generating C# and TypeScript API clients from the OpenAPI spec.
- **web-client**: React (TypeScript) frontend project. Consumes the generated TypeScript API client for type-safe API calls.
- **openapi-spec.yaml**: The OpenAPI specification file used as the source of truth for contract generation.

## Available API Endpoints

| Method | Endpoint             | Description           |
|--------|----------------------|-----------------------|
| GET    | /api/products        | Get all products      |
| GET    | /api/products/{id}   | Get product by ID     |

- **GET /api/products**: Returns a list of all products.
- **GET /api/products/{id}**: Returns a single product by its ID. Returns 404 if not found.

## General Workflow

1. **Edit the OpenAPI spec** (`openapi-spec.yaml`) as needed.
2. **Generate contracts** (C# and TypeScript clients) using NSwag.
3. **Distribute generated clients** to the API server and web client projects.
4. **Run the full stack** using Docker Compose.

## Commands

### 1. Install dependencies (for contract generation)
```sh
cd contracts-nswag
npm install
```

### 2. Generate contracts (C# and TypeScript clients)
```sh
npm run build
```
This will:
- Clean previous outputs
- Run NSwag to generate new clients
- Copy the generated C# client to `api-server/Contracts/`
- Copy the generated TypeScript client to `web-client/src/contracts/`

### 3. Running the full stack with Docker Compose

#### Prerequisites
- Docker and Docker Compose installed
- **AutoMapper license key**: Required for the API server.

#### Start all services
```sh
docker compose up --build -d
```
- The API server will be available at [http://localhost:5050](http://localhost:5050)
- The web client will be available at [http://localhost:5173](http://localhost:5173)

#### Stopping services
```sh
docker compose down -v
```

## Notes on License Key
- The API server requires an AutoMapper license key, which must be set in its `appsettings.json`.
- When running via Docker Compose, remember to set it before building an image. Docker Compose does not use secrets and secure replacement of key is not configured for simplicity.

## Summary
This project provides a robust, automated workflow for keeping backend and frontend API contracts in sync, reducing integration errors and manual work. All contract generation and distribution is handled via scripts and Docker, making onboarding and maintenance easy for new developers. 