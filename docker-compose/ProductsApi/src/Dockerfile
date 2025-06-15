# src/Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /source

# Copy all source code first
COPY ProductsApi/ ProductsApi/
# Restore dependencies after all sources are present
RUN dotnet restore ProductsApi/ProductsApi.csproj

# Copy source code and build
WORKDIR /source/ProductsApi
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Copy published application
COPY --from=build --chown=appuser:appgroup /app/publish .

# Switch to non-root user
USER appuser

EXPOSE 8080
ENTRYPOINT ["dotnet", "ProductsApi.dll"]
