import json
from datetime import datetime
from decimal import Decimal

import oracledb
from sqlalchemy import select, text, or_, func, and_
from sqlalchemy.orm import Session, joinedload

from . import models as premia_models, schemas as premia_schemas
from . import schemas as query_schemas
from ..auth import schemas as auth_schema, models as auth_models
from ..db.crud_base_orcl import CRUDBase, ModelType
from ..quotes.endorsments import schemas as endt_schemas
from ..reports import schemas as report_schemas


# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime to ISO format
        elif isinstance(o, Decimal):
            return float(o)  # Convert Decimal to float (or use str(o) for string)
        return super().default(o)


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

    def validate_vehicle_json(self, oracle_db: Session, search_criteria: dict[str, str]) -> str:
        cursor = oracle_db.connection().connection.cursor()
        p_json = cursor.var(oracledb.STRING)

        cursor.callproc('JICK_UTILS_V2.VALIDATE_VEH', [
            search_criteria["vehicle_reg_no"],
            search_criteria["vehicle_chassis_no"],
            search_criteria["vehicle_engine_no"],
            p_json
        ])
        oracle_db.commit()

        return p_json.getvalue()

    def endt_request_depr(self, oracle_db: Session, endt_init_payload: endt_schemas.EndorsementRequestBase) -> None:
        cursor = oracle_db.connection().connection.cursor()
        # p_ref_number = oracle_db.execute(text('SELECT PGI_INF_FLEX_SYS_ID.NEXTVAL FROM dual')).first()[0]
        p_ref_number = 1
        p_ws_input = json.dumps(endt_init_payload.model_dump())
        p_ws_response_type = cursor.var(oracledb.STRING)
        p_ws_error = cursor.var(oracledb.CURSOR)
        p_ws_response = cursor.var(oracledb.CURSOR)
        p_pol_sys_id = cursor.var(oracledb.NUMBER)
        p_pol_end_idx = cursor.var(oracledb.NUMBER)

        cursor.callproc('PGIPK_INTG_FLEX.PR_PARSE_WS_KEY', [
            p_ref_number,
            p_ws_input,
            p_ws_response_type,
            p_ws_error,
            p_ws_response,
            p_pol_sys_id,
            p_pol_end_idx,
        ])
        oracle_db.commit()

        return p_pol_sys_id.getvalue(), p_pol_end_idx.getvalue()

    def endt_init(self, oracle_db: Session, endt_init_payload: endt_schemas.EndtInit) -> None:
        cursor = oracle_db.connection().connection.cursor()
        p_input_json = json.dumps(endt_init_payload.model_dump(),
                                  default=lambda obj: obj.strftime('%d-%b-%y %H:%M') if isinstance(obj,
                                                                                                   datetime) else obj)

        p_output_cursor = oracle_db.connection().connection.cursor()
        p_ws_error = oracle_db.connection().connection.cursor()
        p_ws_response = oracle_db.connection().connection.cursor()

        p_prem_success = cursor.var(oracledb.STRING)
        p_inst_success = cursor.var(oracledb.STRING)

        cursor.callproc('JICK_UTILS_V2.P_ENDT_INIT', [
            p_input_json,
            p_output_cursor,
            p_ws_error,
            p_ws_response,
        ])
        rows = p_output_cursor.fetchall()
        column_names = [col[0] for col in p_output_cursor.description]
        json_result = [dict(zip(column_names, row)) for row in rows]
        oracle_db.commit()
        if not json_result[0]["STATUS"].startswith("ORA-0000"):
            return json_result

        # cursor.callproc('JICK_UTILS_V2.P_CALC_PREMIUM', [
        #     endt_init_payload.policy_no,
        #     p_prem_success,
        #     p_inst_success
        # ])

        cursor.callproc('JICK_UTILS_V2.P_CALC_PREMIUM', [
            endt_init_payload.policy_no,
            p_output_cursor
        ])
        oracle_db.commit()

        rows = p_output_cursor.fetchall()
        # Fetch column names from cursor description
        column_names = [col[0] for col in p_output_cursor.description]
        # Convert rows to a list of dictionaries (JSON-like structure)
        json_result = [dict(zip(column_names, row)) for row in rows]
        p_output_cursor.close()
        if not json_result[0]["STATUS"].startswith("ORA-0000"):
            return json_result
        # return json.dumps(json_result, indent=4, cls=DateTimeEncoder)
        return json_result

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

    def approve_policy(self, oracle_db: Session, pol_no: str) -> str:
        cursor = oracle_db.connection().connection.cursor()
        p_pol_no = cursor.var(oracledb.STRING)
        p_output_cursor = oracle_db.connection().connection.cursor()

        cursor.callproc('JICK_UTILS_V2.P_APPROVE_POLICY', [
            p_pol_no,
            p_output_cursor
        ])
        oracle_db.commit()
        rows = p_output_cursor.fetchall()
        # Fetch column names from cursor description
        column_names = [col[0] for col in p_output_cursor.description]
        # Convert rows to a list of dictionaries (JSON-like structure)
        json_result = [dict(zip(column_names, row)) for row in rows]
        p_output_cursor.close()
        if not json_result[0]["STATUS"].startswith("ORA-0000"):
            return json_result
        # return json.dumps(json_result, indent=4, cls=DateTimeEncoder)
        return json_result

    def run_report(self, oracle_db: Session, report_params: report_schemas.ReportParams) -> str:
        cursor = oracle_db.connection().connection.cursor()
        output_cursor = oracle_db.connection().connection.cursor()
        search_criteria = list(report_params.search_criteria.model_dump(exclude_unset=True).values())
        cursor.callproc(report_params.proc_name, [*search_criteria, output_cursor])
        # cursor.callproc('JICK_UTILS_V2.P_CUST_PROD_RPT', ['150091', '01-SEP-2011', '30-OCT-2024', 1, 10, output_cursor])

        rows = output_cursor.fetchall()
        oracle_db.commit()
        # Fetch column names from cursor description
        column_names = [col[0] for col in output_cursor.description]
        # Convert rows to a list of dictionaries (JSON-like structure)
        json_result = [dict(zip(column_names, row)) for row in rows]
        output_cursor.close()
        # return json.dumps(json_result, indent=4, cls=DateTimeEncoder)
        return json_result

    def query_policy(self, oracle_db: Session, search_criteria: dict[str, str]) -> list[premia_models.Policy]:
        stmt = (
            select(premia_models.Policy)
            .options(
                joinedload(premia_models.Policy.policycharge_collection),
                joinedload(premia_models.Policy.policysection_collection)
                .joinedload(premia_models.PolicySection.policyrisk_collection)
                .joinedload(premia_models.PolicyRisk.policycover_collection)
            )
            .where(premia_models.Policy.pol_no == search_criteria["pol_no"])
        )
        result = oracle_db.execute(stmt)
        pol_list = result.unique().scalars().all()
        policy_list = [query_schemas.PolicyQuerySchema.model_validate(pol_instance) for pol_instance in pol_list]

        return policy_list


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

    def get_customer_by_all(self, oracle_db: Session, search_criteria: dict[str, str]) -> list[premia_models.Customer]:
        query = select(premia_models.Customer)
        where_criteria = conditions = [getattr(premia_models.Customer, attr) == value for attr, value in
                                       search_criteria.items()]

        if where_criteria:
            query = query.where(*where_criteria)

        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        query_str = str(compiled_query)
        # Set the session-specific parameters for case-insensitivity
        # oracle_db.execute(text("ALTER SESSION SET NLS_COMP=LINGUISTIC"))
        # oracle_db.execute(text("ALTER SESSION SET NLS_SORT=BINARY_CI"))
        result = oracle_db.execute(query)
        customer_list = result.scalars().all()

        return customer_list

    def get_customer_by_any(self, oracle_db: Session, search_criteria: dict[str, str]) -> list[premia_models.Customer]:
        query = select(self.model)
        where_criteria = [getattr(premia_models.Customer, attr) == value
                          for attr, value in search_criteria.items()]

        # Add the AND condition to check the NVL logic
        and_condition = func.nvl(func.trunc(premia_models.Customer.cust_eff_to_dt),
                                 func.trunc(func.sysdate()) + 1) > func.trunc(
            func.sysdate())

        if where_criteria:
            query = query.where(and_(and_condition, or_(*where_criteria)))

        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        query_str = str(compiled_query)
        result = oracle_db.execute(query)
        customer_list = result.scalars().all()

        return customer_list

    def get_new_cust_code(self, non_async_oracle_db: Session, cust_in: auth_models.User) -> str:
        cust_cc_prefix = cust_in.premia_cust_payload["cust_cc_prefix"]
        query = select(premia_models.DocNumberRange).where(
            premia_models.DocNumberRange.dnr_level_01 == cust_cc_prefix).with_for_update(
            nowait=False, of=premia_models.DocNumberRange.dnr_curr_no)

        result = non_async_oracle_db.execute(query)
        doc_num_rng_obj = result.scalars().all()[0]
        next_no = doc_num_rng_obj.dnr_curr_no + 1
        doc_num_rng_obj = self.update(non_async_oracle_db, db_obj=doc_num_rng_obj, obj_in={"dnr_curr_no": next_no})

        return f"{cust_cc_prefix}{next_no:06}"


class CRUDReceiptStage(
    CRUDBase[premia_models.ReceiptStaging, premia_models.ReceiptStagingBase, premia_models.ReceiptStagingBase]):
    def create_v1(
            self, oracle_db: Session, *, obj_in: premia_models.ReceiptStagingBase
    ) -> premia_models.ReceiptStaging:
        receipt_stage_dict = obj_in.model_dump(exclude_unset=True)
        return super().create_v1(oracle_db, obj_in=receipt_stage_dict)


policy = CRUDPolicy(premia_models.Policy)
customer = CRUDCustomer(premia_models.Customer)
receipt_stage = CRUDReceiptStage(premia_models.ReceiptStaging)
