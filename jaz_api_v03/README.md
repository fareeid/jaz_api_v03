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
    - run - alembic revision --autogenerate -m "create update stamp"
    - run - alembic upgrade head or alembic downgrade head

Logging construct
    - import logging
    - log = logging.getLogger("uvicorn")
    - log.info("Test logging from crud_base get...")

```

```
{
   "quot_ref":"5773197888",
   "quot_assr_name": "John Doe",
   "quot_assr_nic": "3000211",
   "quot_assr_pin": "P00892519Y",
   "quot_assr_phone": "2547xxxxxxxx",
   "quot_assr_email": "test@mfs.co.ke",
   "quot_paymt_ref":"RIS1VW7M7H",
   "quot_paymt_date":"2023-09-26T09:53:00",
   "proposals":[
      {
         "prop_sr_no":1,
         "prop_paymt_ref":"RIS1VW7M7H",
         "prop_paymt_date":"2023-09-26T09:53:00",
         "pol_quot_no":"5773197888",
         "pol_comp_code":"001",
         "pol_divn_code":"101",
         "pol_prod_code":"5006",
         "pol_type":"5006",
         "pol_cust_code":"K21006439",
         "pol_fm_dt":"2023-09-26T00:00:00",
         "pol_to_dt":"2024-09-27T00:00:00",
         "pol_dflt_si_curr_code":"KES",
         "pol_prem_curr_code":"KES",
         "proposalsections":[
            {
               "sec_sr_no":1,
               "psec_sec_code":"500601",
               "proposalrisks":[
                  {
                     "risk_sr_no":1,
                     "prai_data_18":"Kenya",
                     "prai_code_03":"503",
                     "prai_desc_09":"Residential",
                     "prai_flexi":{
                        "premises":{
                           "prai_data_18":"Kenya"
                        },
                        "all_risk_type_code":{
                           "prai_code_03":"503"
                        },
                        "all_risk_type_desc":{
                           "prai_desc_09":"Residential"
                        }
                     },
                     "proposalcovers":[
                        {
                           "cvr_sr_no":1,
                           "prc_code":"3553",
                           "prc_rate":1.75,
                           "prc_rate_per":1000.0,
                           "prc_si_curr_code":"KES",
                           "prc_prem_curr_code":"KES",
                           "prc_si_fc":50000.0,
                           "prc_prem_fc":875.0
                        }
                     ],
                     "proposalsmis":[
                        {
                           "smi_sr_no":1,
                           "prs_smi_code":"9000004",
                           "prs_rate":1.75,
                           "prs_rate_per":100.0,
                           "prs_si_fc":30000.0,
                           "prs_prem_fc":500.0,
                           "prs_smi_desc":"Details(name='COOKERS', make='ARMCO', model='CHEST FREEZER AF-26K', serial_num='0FYJ4ABH700044V45')"
                        },
                        {
                           "smi_sr_no":2,
                           "prs_smi_code":"9000006",
                           "prs_rate":1.75,
                           "prs_rate_per":100.0,
                           "prs_si_fc":20000.0,
                           "prs_prem_fc":400.0,
                           "prs_smi_desc":"Details(name='FREEZERS', make='ARMCO', model='316LTR CHEST FREEZER#BCF3316', serial_num='0FYJ4ABH700044V4005')"
                        }
                     ]
                  }
               ]
            }
         ],
         "proposalcharges":[
            {
               "chg_sr_no":1,
               "pchg_code":"2001",
               "pchg_type":"002",
               "pchg_perc":40,
               "pchg_chg_fc":40.0,
               "pchg_prem_curr_code":"KES",
               "pchg_rate_per":1
            },
            {
               "chg_sr_no":2,
               "pchg_code":"1004",
               "pchg_type":"005",
               "pchg_perc":0.25,
               "pchg_chg_fc":12.0,
               "pchg_prem_curr_code":"KES",
               "pchg_rate_per":100.0
            },
            {
               "chg_sr_no":3,
               "pchg_code":"2004",
               "pchg_type":"002",
               "pchg_perc":0.2,
               "pchg_chg_fc":11.0,
               "pchg_prem_curr_code":"KES",
               "pchg_rate_per":100.0
            }
         ]
      }
   ]
}

def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
	obj_in_data = jsonable_encoder(obj_in)
	db_obj = self.model(**obj_in_data)  # type: ignore
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	return db_obj
	

def create(self, db: Session, *, obj_in: UserCreate) -> User:
	db_obj = User(
		email=obj_in.email,
		hashed_password=get_password_hash(obj_in.password),
		full_name=obj_in.full_name,
		is_superuser=obj_in.is_superuser,
	)
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	return db_obj
```