import oracledb
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import models as premia_models, schemas as premia_schemas
from ..auth import schemas as auth_schema, models as auth_models
from ..db.crud_base_orcl import CRUDBase, ModelType


class CRUDPolicy(CRUDBase[premia_models.Policy, premia_models.PolicyBase, premia_schemas.PolicyUpdate]):
    def create_v1(
            self, oracle_db: Session, *, obj_in: premia_models.PolicyBase
    ) -> premia_models.Policy:
        # policy_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))
        # sections_list = obj_in.policysection_collection
        # print(sections_list)
        # sections_list_db = [
        #     premia_models.PolicySection(**section.model_dump(exclude_unset=True))
        #     for section in sections_list
        # ]
        # print(sections_list_db)

        policy_dict = obj_in.model_dump(exclude_unset=True)
        # policy_dict["policysection_collection"] = sections_list_db
        # policy_dict = {k: v for k, v in obj_in.items() if v and v!=''}
        return super().create_v1(oracle_db, obj_in=policy_dict)

    def get_sys_id(self, oracle_db: Session, pgi_sequence_name: str) -> int:
        query = text(f"SELECT {pgi_sequence_name}.NEXTVAL FROM DUAL")
        # query = text(f"SELECT nextval('{pgi_sequence_name}');")
        result = oracle_db.execute(query)
        sys_id = result.first()[0]
        return sys_id

    def get_pol_no(self, oracle_db: Session, proposal: dict[str, str]) -> str:
        cursor = oracle_db.connection().connection.cursor()
        p_pol_sys_id: int = cursor.var(oracledb.NUMBER)
        p_pol_no = cursor.var(oracledb.STRING)
        p_pol_no_avl = cursor.var(oracledb.STRING)

        cursor.callproc('PGIPK_DOCUMENT_NUMBER.PR_GENERATE_DOC_NUMBER', [
            proposal["pol_ds_type"],  # First input parameter
            proposal["pol_ds_code"],  # Second input parameter
            proposal["pol_comp_code"],  # Third input parameter
            proposal["pol_dept_code"],  # Fourth input parameter
            proposal["pol_divn_code"],  # Fifth input parameter
            proposal["pol_sys_id"],  # Sixth input parameter 14937115, #
            p_pol_no,  # output parameter 2
            p_pol_no_avl  # Output parameter 3
        ])
        oracle_db.commit()

        # cursor.callproc('PGIPK_DOCUMENT_NUMBER.PR_GENERATE_DOC_NUMBER', [
        #     '2',  # First input parameter
        #     '10-PL-01-001',  # Second input parameter (replace with the actual value)
        #     '001',  # Third input parameter
        #     '10',  # Fourth input parameter
        #     '118',  # Fifth input parameter
        #     14937115,  # output parameter 1
        #     p_pol_no,  # output parameter 2
        #     p_pol_no_avl  # Output parameter 3
        # ])

        return p_pol_no.getvalue()

    def policy_process_json(self, oracle_db: Session, pol_trans: premia_models.Policy) -> str:
        cursor = oracle_db.connection().connection.cursor()
        p_pol_sys_id: int = cursor.var(oracledb.NUMBER)
        p_prem_success = cursor.var(oracledb.STRING)
        p_json = cursor.var(oracledb.STRING)

        cursor.callproc('JICK_UTILS_V2.PROCESS_PORTAL_NEW_POLICIES', [
            pol_trans.pol_ds_type,
            pol_trans.pol_ds_code,
            pol_trans.pol_comp_code,
            pol_trans.pol_dept_code,
            pol_trans.pol_divn_code,
            pol_trans.pol_sys_id,
            pol_trans.pol_end_no_idx,
            pol_trans.pol_end_sr_no,
            pol_trans.pol_fm_dt,
            pol_trans.pol_prod_code,
            pol_trans.pol_inst_code,
            p_json
        ])
        oracle_db.commit()

        return p_json.getvalue()

    def receipt_process_json(self, oracle_db: Session, receipt_stage: premia_models.ReceiptStaging) -> str:
        cursor = oracle_db.connection().connection.cursor()
        p_json = cursor.var(oracledb.STRING)

        cursor.callproc('JICK_UTILS_V2.AUTO_RECEIPT', [
            receipt_stage.r_sys_id,
            p_json
        ])
        oracle_db.commit()

        return p_json.getvalue()

    def calc_premium(self, oracle_db: Session, pol_trans: premia_models.Policy) -> str:
        cursor = oracle_db.connection().connection.cursor()
        p_pol_sys_id: int = cursor.var(oracledb.NUMBER)
        p_prem_success = cursor.var(oracledb.STRING)
        p_inst_success = cursor.var(oracledb.STRING)

        cursor.callproc('PGIPK_PREMIUM_CALC.P_CALC_PREMIUM', [
            pol_trans.pol_comp_code,
            pol_trans.pol_divn_code,
            pol_trans.pol_dept_code,
            pol_trans.pol_sys_id,
            pol_trans.pol_end_no_idx,
            pol_trans.pol_end_sr_no,
            pol_trans.pol_fm_dt,
            pol_trans.pol_prod_code,
            'B',
            pol_trans.pol_ds_type,
            pol_trans.pol_inst_code,
            p_prem_success,  # output parameter 2
            p_inst_success  # Output parameter 3
        ])
        oracle_db.commit()

        return p_prem_success.getvalue()


class CRUDCustomer(
    CRUDBase[premia_models.Customer, auth_schema.UserCreate, auth_schema.UserUpdate]
):
    def create_v1(self, nonasync_oracle_db: Session, obj_in: premia_models.CustomerBase) -> ModelType:
        # customer_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))
        customer_dict = obj_in.model_dump(exclude_unset=True)
        return super().create_v1(nonasync_oracle_db, obj_in=customer_dict)

    def get_cust_by_pin(self, oracle_db: Session, pin: str) -> list[premia_models.Customer]:
        result = oracle_db.execute(
            select(self.model).where(self.model.cust_civil_id == pin)
        )
        return list(result.scalars().all())

    def get_customer(self, oracle_db: Session, search_criteria: dict[str, str]) -> list[premia_models.Customer]:
        query = select(premia_models.Customer)
        where_criteria = conditions = [getattr(premia_models.Customer, attr) == value for attr, value in
                                       search_criteria.items()]

        if where_criteria:
            query = query.where(*where_criteria)

        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        query_str = str(compiled_query)
        result = oracle_db.execute(query)
        customer_list = result.scalars().all()

        return customer_list

    def get_cust_code(self, non_async_oracle_db: Session, cust_in: auth_models.User) -> str:
        cust_cc_prefix = cust_in.premia_cust_payload["cust_cc_prefix"]
        query = select(premia_models.DocNumberRange).where(
            premia_models.DocNumberRange.dnr_level_01 == cust_cc_prefix).with_for_update(
            nowait=False, of=premia_models.DocNumberRange.dnr_curr_no)

        result = non_async_oracle_db.execute(query)
        doc_num_rng_obj = result.scalars().all()[0]
        next_no = doc_num_rng_obj.dnr_curr_no + 1
        doc_num_rng_obj = self.update(non_async_oracle_db, db_obj=doc_num_rng_obj, obj_in={"dnr_curr_no": next_no})

        return f"{cust_cc_prefix}{next_no:06}"


class CRUDReceiptStage(CRUDBase[premia_models.ReceiptStaging, premia_models.ReceiptStagingBase, premia_models.ReceiptStagingBase]):
    def create_v1(
            self, oracle_db: Session, *, obj_in: premia_models.ReceiptStagingBase
    ) -> premia_models.ReceiptStaging:

        receipt_stage_dict = obj_in.model_dump(exclude_unset=True)
        return super().create_v1(oracle_db, obj_in=receipt_stage_dict)


policy = CRUDPolicy(premia_models.Policy)
customer = CRUDCustomer(premia_models.Customer)
receipt_stage = CRUDReceiptStage(premia_models.ReceiptStaging)
