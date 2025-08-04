# Configuración de GitHub Environments

Este documento explica cómo configurar los GitHub Environments para el workflow de CI/CD.

## ¿Qué son GitHub Environments?

Los GitHub Environments te permiten:
- Configurar variables de entorno específicas por ambiente
- Gestionar secretos de forma segura
- Establecer reglas de protección (reviews, timeouts)
- Controlar el acceso a diferentes entornos

## Configuración de Environments

### 1. Development Environment

**Configuración en GitHub:**
1. Ve a tu repositorio → Settings → Environments
2. Crea un nuevo environment llamado `development`
3. Configura las siguientes variables:

**Variables (Variables):**
```
ENVIRONMENT_NAME=development
LOG_LEVEL=DEBUG
FEATURE_FLAGS=enabled
```

**Secretos (Secrets):**
```
DATABASE_URL=mysql://dev_user:dev_pass@dev-db:3306/dev_db
API_KEY=dev_api_key_123
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

**Reglas de protección:**
- No configurar reglas especiales para desarrollo

### 2. Staging Environment

**Configuración en GitHub:**
1. Crea un environment llamado `staging`
2. Configura las siguientes variables:

**Variables (Variables):**
```
ENVIRONMENT_NAME=staging
LOG_LEVEL=INFO
FEATURE_FLAGS=enabled
```

**Secretos (Secrets):**
```
DATABASE_URL=mysql://staging_user:staging_pass@staging-db:3306/staging_db
API_KEY=staging_api_key_456
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

**Reglas de protección:**
- Required reviewers: 1
- Wait timer: 5 minutes
- Deployment branches: `staging`

### 3. Production Environment

**Configuración en GitHub:**
1. Crea un environment llamado `production`
2. Configura las siguientes variables:

**Variables (Variables):**
```
ENVIRONMENT_NAME=production
LOG_LEVEL=WARNING
FEATURE_FLAGS=disabled
```

**Secretos (Secrets):**
```
DATABASE_URL=mysql://prod_user:prod_pass@prod-db:3306/prod_db
API_KEY=prod_api_key_789
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

**Reglas de protección:**
- Required reviewers: 2
- Wait timer: 10 minutes
- Deployment branches: `main`
- Environment protection rules: Enabled

## Flujo de Trabajo

### Desarrollo (dev branch)
```bash
git checkout dev
git add .
git commit -m "Nueva funcionalidad"
git push origin dev
```

**Resultado:**
- Se ejecutan las pruebas
- Si las pruebas pasan, se despliega automáticamente a development
- Se envía notificación a Slack

### Staging (staging branch)
```bash
git checkout staging
git merge dev
git push origin staging
```

**Resultado:**
- Se ejecutan las pruebas
- Si las pruebas pasan, se despliega a staging (con wait timer y review)
- Se envía notificación a Slack

### Producción (main branch)
```bash
git checkout main
git merge staging
git push origin main
```

**Resultado:**
- Se ejecutan las pruebas
- Si las pruebas pasan, se despliega a producción (con wait timer y 2 reviews requeridos)
- Se envía notificación a Slack

## Variables de Entorno Disponibles

En cada job que use un environment, tendrás acceso a:

### Secrets
- `${{ secrets.DATABASE_URL }}`
- `${{ secrets.API_KEY }}`
- `${{ secrets.SLACK_WEBHOOK }}`

### Variables
- `${{ vars.ENVIRONMENT_NAME }}`
- `${{ vars.LOG_LEVEL }}`
- `${{ vars.FEATURE_FLAGS }}`

## Ejemplo de Uso en Código

```python
import os

# Acceder a variables de entorno
database_url = os.environ.get('DATABASE_URL')
api_key = os.environ.get('API_KEY')
environment = os.environ.get('ENVIRONMENT_NAME')

print(f"Running in {environment} environment")
print(f"Database: {database_url}")
print(f"API Key: {api_key}")
```

## Notificaciones

El workflow incluye notificaciones automáticas a Slack para:
- Inicio de deployment
- Éxito de deployment
- Fallo de deployment

## Troubleshooting

### Error: Environment not found
- Verifica que el environment esté creado en GitHub
- Asegúrate de que el nombre coincida exactamente

### Error: Required reviewers not satisfied
- Para staging y production, necesitas aprobación manual
- Ve a la pestaña "Actions" y busca el deployment pendiente

### Error: Wait timer not expired
- Los environments tienen timers de espera configurados
- Espera el tiempo especificado antes de que se ejecute el deployment 