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

## Cloud Build desde GitHub

El repo incluye [cloudbuild.yaml](/Users/davidgutierrez/Documents/GitHub/flowdexAPI/cloudbuild.yaml) para usar un trigger de Cloud Build conectado a GitHub.

Configura el trigger para que use ese archivo y define estas sustituciones:

- `_REGION=europe-southwest1`
- `_AR_REPOSITORY=flowdex`
- `_SERVICE_NAME=flowdex-api`
- `_INSTANCE_CONNECTION_NAME=flowdex-490012:europe-southwest1:flowdex`
- `_DB_NAME=postgres`
- `_DB_USER=postgres`
- `_RUNTIME_SERVICE_ACCOUNT=flowdex-api@flowdex-490012.iam.gserviceaccount.com`
- `_SECRET_KEY_SECRET=flowdex-secret`
- `_DB_PASSWORD_SECRET=flowdex-db-password`

El pipeline hace:

- `docker build` usando el `Dockerfile` del repo
- `docker push` a Artifact Registry
- `gcloud run deploy` al servicio Cloud Run

Permisos mínimos para la service account de Cloud Build:

- `Cloud Run Admin`
- `Service Account User`
- `Artifact Registry Writer`
- `Secret Manager Secret Accessor`
- `Cloud SQL Client`

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
- El despliegue desde Cloud Build usa imagen inmutable por commit SHA.
