# src/Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /source

# Copy all source code first
COPY . ProductsApi/
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

# Install ICU(International Components for Unicode) for globalization support. Alpine distribution does not include it by default.
RUN apk add --no-cache icu-libs
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false

# Copy published application
COPY --from=build --chown=appuser:appgroup /app/publish .

# Switch to non-root user
USER appuser

EXPOSE 8080
ENTRYPOINT ["dotnet", "ProductsApi.dll"]