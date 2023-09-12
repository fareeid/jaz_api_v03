# jaz_api_v03

1. az group create --name c --location northeurope
2. az acr create --resource-group jazk-api-rg --name jazkapiregistry --sku Basic --admin-enabled                ------------------------Cannot contain dashes
3. az acr credential show --name jazkapiregistry --resource-group jazk-api-rg
4. az acr login --name jazkapiregistry
5. az acr build --registry jazkapiregistry --resource-group jazk-api-rg --image jaz_api_v03:latest .
6. az acr build --registry jazkapiregistry --resource-group jazk-api-rg --file Dockerfile.Azure --image jaz_api_v03:latest jaz_api_v03
7. az acr repository list --name jazkapiregistry
8. az containerapp env create --name jazk-api-env --resource-group jazk-api-rg --location northeurope
9. az containerapp create `
    --name jazk-api-app `
    --resource-group jazk-api-rg `
    --image jazkapiregistry.azurecr.io/jaz_api_v03:latest `
    --environment jazk-api-env `
    --ingress external `
    --target-port 8081 `
    --registry-server jazkapiregistry.azurecr.io `
    --registry-username jazkapiregistry `
    --registry-password 7T/VfhS1iuxAF2YKNYPjX9h8SvOMpCJkkbyzHZBOzj+ACRBPFERz `
    --env-vars "ENV_VAR_ONE=1 ENV_VAR_TWO=2 ENV_SECRET=SECRETREF:MY_SECRET" `
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

  * ContainerAppSystemLogs_CL | where RevisionName_s == "jazk-api-app--xg82nuf"
