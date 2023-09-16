# jaz_api_v03
```
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
    --target-port 3100 `
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

https://github.com/fareeid/jaz_api_v02/blob/main/app/config.py
https://github.com/fareeid/fastapi-tdd/blob/main/project/app/config.py
https://github.com/fareeid/jaz_api_v02/blob/main/app/config.py
https://github.com/fareeid/fastapi/blob/master/pyproject.toml
https://github.com/fareeid/tiangolo/blob/master/backend/app/app/core/config.py

```
Adding Alembic functionality

Intialize alembic with async template
    - invoke container bash using docker-compose exec web bash
    - run - alembic init -t async migrations   ## Don't use docker-compose exec web  due to path issues
    - comment out in alembic.ini - #### sqlalchemy.url  = driver://user:pass@localhost/dbname
    - update migrations/env.py with the following
        from app.db import Base # noqa
        target_metadata = Base.metadata

        # Add this function that constructs the db url from settings having disabled it in alembic.ini
        def get_url():
            from fastapi import Depends
            from src.core.config import Settings, get_settings
            settings: Settings = Depends(get_settings)

            # user = settings.POSTGRES_USER
            # password = settings.POSTGRES_PASSWORD
            # server = settings.POSTGRES_SERVER
            # db = settings.POSTGRES_DB
            # return f"postgresql://{user}:{password}@{server}/{db}"
            return settings.SQLALCHEMY_DATABASE_URI
    - update def run_migrations_offline() to use get_url instead of alembic.ini connection string
    - update async def run_async_migrations() to use get_url instead of alembic.ini connection string
    - run - alembic revision --autogenerate -m "init"
    - run - alembic upgrade head or alembic downgrade head

```