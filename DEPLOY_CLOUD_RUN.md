# Deploy Cloud Run

La API queda preparada para desplegarse en Cloud Run sin modificar el esquema de Cloud SQL.

## Variables

Usa estas variables de entorno en Cloud Run:

- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES=60`
- `INSTANCE_CONNECTION_NAME=flowdex-490012:europe-southwest1:flowdex`
- `DB_NAME=postgres`
- `DB_USER=postgres`
- `DB_PASSWORD`

No configures `DATABASE_URL` si quieres usar el socket montado de Cloud SQL.

## Cloud SQL

Adjunta la instancia de Cloud SQL al servicio de Cloud Run:

- instancia: `flowdex-490012:europe-southwest1:flowdex`

La aplicación construye automáticamente la conexión asyncpg por socket:

- host socket: `/cloudsql/flowdex-490012:europe-southwest1:flowdex`

## Build

```bash
gcloud builds submit --tag europe-southwest1-docker.pkg.dev/PROJECT_ID/REPOSITORY/flowdex-api:latest
```

## Deploy

```bash
gcloud run deploy flowdex-api \
  --image europe-southwest1-docker.pkg.dev/PROJECT_ID/REPOSITORY/flowdex-api:latest \
  --region europe-southwest1 \
  --platform managed \
  --allow-unauthenticated \
  --add-cloudsql-instances flowdex-490012:europe-southwest1:flowdex \
  --set-env-vars ACCESS_TOKEN_EXPIRE_MINUTES=60,INSTANCE_CONNECTION_NAME=flowdex-490012:europe-southwest1:flowdex,DB_NAME=postgres,DB_USER=postgres \
  --set-secrets SECRET_KEY=flowdex-secret:latest,DB_PASSWORD=flowdex-db-password:latest
```

## Notas

- El contenedor ya no ejecuta `create_all` ni `alembic stamp` al arrancar.
- Cloud Run usará `PORT`, y local seguirá usando `8000`.
- Hay un endpoint de salud en `/healthz`.
