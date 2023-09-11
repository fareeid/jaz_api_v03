# jaz_api_v03

1. az group create --name jazk-api-rg --location northeurope
2. az acr create --resource-group jazk-api-rg --name jazkapiregistry --sku Basic --admin-enabled                ------------------------Cannot contain dashes
3. az acr credential show --name jazkapiregistry --resource-group jazk-api-rg
4. az acr login --name jazkapiregistry
5. az acr build --registry jazkapiregistry --resource-group jazk-api-rg --image jaz_api_v03:latest .
6. az acr repository list --name jazkapiregistry
7. az containerapp env create --name jazk-api-container-env --resource-group jazk-api-rg --location northeurope
8. az containerapp create \
    --name python-container-app \
    --resource-group pythoncontainer-rg \
    --image <registry-name>.azurecr.io/pythoncontainer:latest \
    --environment python-container-env \
    --ingress external \
    --target-port 8000 \
    --registry-server <registry-name>.azurecr.io \
    --registry-username <registry-username> \
    --registry-password <registry-password> \
    --env-vars <env-variable-string>
    --query properties.configuration.ingress.fqdn


  * Use quickstart image → Unselect checkbox.
  * Name → python-container-app.
  * Image Source → Select Azure Container Registry.
  * Registry → Select the name of registry you created earlier.
  * Image name → Select pythoncontainer (the name of the image you built).
  * Image tag → Select latest.
  * HTTP Ingress → Select checkbox (enabled).
  * Ingress traffic → Select Accepting traffic from anywhere.
  * Target port→ Set to 8000 for Django or 5000 for Flask.
