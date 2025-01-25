from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict


class PolicyAcntDocQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ad_sys_id:Union[int, None] = None
    ad_tran_sys_id:Union[int, None] = None
    ad_pol_sys_id:Union[int, None] = None
    ad_end_no_idx:Union[int, None] = None
    ad_end_sr_no:Union[int, None] = None
    ad_doc_type:Union[str, None] = None
    ad_tran_type:Union[str, None] = None
    ad_tran_code:Union[str, None] = None
    ad_acnt_year:Union[int, None] = None
    ad_doc_no:Union[int, None] = None
    ad_doc_dt:Union[datetime, None] = None
    ad_int_ent_yn:Union[str, None] = None
    ad_drcr_flag:Union[str, None] = None
    ad_curr_code:Union[str, None] = None
    ad_amt_fc:Union[float, None] = None
    ad_amt_lc_1:Union[float, None] = None
    ad_narration:Union[str, None] = None
    ad_main_acnt_code:Union[str, None] = None
    ad_sub_acnt_code:Union[str, None] = None


class PolicyChargeQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pchg_sys_id: Union[int, None] = None
    pchg_pol_sys_id: Union[int, None] = None
    pchg_end_no_idx: Union[int, None] = None
    pchg_end_sr_no: Union[int, None] = None
    pchg_code: Union[str, None] = None
    pchg_type: Union[str, None] = None
    pchg_perc: Union[float, None] = None
    pchg_rate_per: Union[float, None] = None
    pchg_chg_fc: Union[float, None] = None
    pchg_chg_lc_1: Union[float, None] = None


class PolicyCoverQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    prc_sys_id: Union[int, None] = None
    prc_pol_sys_id: Union[int, None] = None
    prc_end_no_idx: Union[int, None] = None
    prc_end_sr_no: Union[int, None] = None
    prc_lvl1_sys_id: Union[int, None] = None
    prc_sr_no: Union[int, None] = None
    prc_code: Union[str, None] = None
    prc_desc: Union[str, None] = None
    prc_rate: Union[float, None] = None
    prc_rate_per: Union[float, None] = None
    prc_si_fc: Union[float, None] = None
    prc_si_lc_1: Union[float, None] = None
    prc_prem_fc: Union[float, None] = None
    prc_prem_lc_1: Union[float, None] = None
    prc_eff_fm_dt: Union[datetime, None] = None
    prc_eff_to_dt: Union[datetime, None] = None
    prc_end_eff_fm_dt: Union[datetime, None] = None


class PolicyRiskQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    prai_sys_id: Union[int, None] = None
    prai_pol_sys_id: Union[int, None] = None
    prai_end_no_idx: Union[int, None] = None
    prai_end_sr_no: Union[int, None] = None
    prai_risk_lvl_no: Union[int, None] = None
    prai_lvl1_sys_id: Union[int, None] = None
    prai_lvl1_sr_no: Union[int, None] = None
    prai_lvl2_sys_id: Union[int, None] = None
    prai_lvl2_sr_no: Union[int, None] = None
    prai_si_fc: Union[float, None] = None
    prai_si_lc_1: Union[float, None] = None
    prai_prem_fc: Union[float, None] = None
    prai_prem_lc_1: Union[float, None] = None
    prai_eff_fm_dt: Union[datetime, None] = None
    prai_eff_to_dt: Union[datetime, None] = None
    prai_end_eff_fm_dt: Union[datetime, None] = None
    prai_code_01: Union[str, None] = None
    prai_code_03: Union[str, None] = None
    prai_code_04: Union[str, None] = None
    prai_code_05: Union[str, None] = None
    prai_code_14: Union[str, None] = None
    prai_num_01: Union[int, None] = None
    prai_num_02: Union[int, None] = None
    prai_num_03: Union[int, None] = None
    prai_num_04: Union[int, None] = None
    prai_data_01: Union[str, None] = None
    prai_data_02: Union[str, None] = None
    prai_data_03: Union[str, None] = None
    prai_data_05: Union[str, None] = None
    prai_risk_id: Union[str, None] = None
    prai_risk_sr_no: Union[int, None] = None
    prai_num_08: Union[int, None] = None
    prai_num_09: Union[int, None] = None
    prai_num_14: Union[int, None] = None
    prai_remarks_10: Union[str, None] = None
    prai_date_21: Union[datetime, None] = None
    prai_date_22: Union[datetime, None] = None
    policycover_collection: list[PolicyCoverQuerySchema] = []


class PolicySectionQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    psec_sys_id: Union[int, None] = None
    psec_pol_sys_id: Union[int, None] = None
    psec_end_no_idx: Union[int, None] = None
    psec_end_sr_no: Union[int, None] = None
    psec_sec_code: Union[str, None] = None
    psec_eff_fm_dt: Union[datetime, None] = None
    psec_eff_to_dt: Union[datetime, None] = None
    policyrisk_collection: list[PolicyRiskQuerySchema] = []


class PolicyQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pol_sys_id: Union[int, None] = None
    pol_end_no_idx: Union[int, None] = None
    pol_end_sr_no: Union[int, None] = None
    pol_comp_code: Union[str, None] = None
    pol_divn_code: Union[str, None] = None
    pol_dept_code: Union[str, None] = None
    pol_class_code: Union[str, None] = None
    pol_prod_code: Union[str, None] = None
    pol_cust_code: Union[str, None] = None
    pol_assr_code: Union[str, None] = None
    pol_assr_name: Union[str, None] = None
    pol_no: Union[str, None] = None
    pol_issue_dt: Union[datetime, None] = None
    pol_fm_dt: Union[datetime, None] = None
    pol_to_dt: Union[datetime, None] = None
    pol_dflt_si_curr_code: Union[str, None] = None
    pol_prem_curr_code: Union[str, None] = None
    pol_prem_lc_1: Union[float, None] = None
    pol_end_type: Union[str, None] = None
    pol_end_code: Union[str, None] = None
    pol_end_no: Union[str, None] = None
    pol_end_dt: Union[datetime, None] = None
    pol_end_eff_fm_dt: Union[datetime, None] = None
    pol_end_eff_to_dt: Union[datetime, None] = None
    pol_end_desc: Union[str, None] = None
    pol_remarks: Union[str, None] = None
    pol_hypothecation_yn: Union[str, None] = None
    pol_quot_sys_id: Union[int, None] = None
    pol_quot_no: Union[str, None] = None
    pol_ren_pol_sys_id: Union[int, None] = None
    pol_ren_pol_no: Union[str, None] = None
    pol_ren_cnt_sr_no: Union[int, None] = None
    pol_no_risk: Union[int, None] = None
    pol_no_section: Union[int, None] = None
    pol_sts: Union[str, None] = None
    pol_appr_sts: Union[str, None] = None
    pol_appr_dt: Union[datetime, None] = None
    pol_mode_of_pay: Union[str, None] = None
    pol_si_lc_1: Union[float, None] = None
    pol_uw_year: Union[int, None] = None
    pol_flex_01: Union[str, None] = None
    pol_flex_09: Union[str, None] = None
    pol_flex_13: Union[str, None] = None
    pol_flex_14: Union[str, None] = None
    pol_flex_16: Union[str, None] = None
    pol_flex_17: Union[str, None] = None
    pol_flex_18: Union[str, None] = None
    pol_acnt_doc_dt: Union[datetime, None] = None
    pol_old_pol_no: Union[str, None] = None
    policycharge_collection: list[PolicyChargeQuerySchema] = []
    policysection_collection: list[PolicySectionQuerySchema] = []
    policyacntdoc_collection: list[PolicyAcntDocQuerySchema] = []
