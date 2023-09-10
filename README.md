# jaz_api_v03

az group create --name jazk-api-rg --location northeurope
az acr create --resource-group jazk-api-rg --name jazkapiregistry --sku Basic --admin-enabled                ------------------------Cannot contain dashes
az acr credential show --name jazkapiregistry --resource-group jazk-api-rg
az acr login --name jazkapiregistry
az acr build --registry jazkapiregistry --resource-group jazk-api-rg --image jaz_api_v03:latest .
az acr repository list --name jazkapiregistry
