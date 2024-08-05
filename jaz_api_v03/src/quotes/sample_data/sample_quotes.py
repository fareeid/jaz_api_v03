import json
import random
import string
from typing import Any

from faker import Faker
from fastapi.encoders import jsonable_encoder

from .. import schemas as quote_schemas
from ..vendors_api import schemas as vendor_schemas
from ...core.dependencies import aes_encrypt

fake = Faker()


def create_charges_list() -> list[quote_schemas.ProposalChargeCreate]:
    charges_list = []
    stamp_duty_obj = quote_schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="2003",
        pchg_type="002",
        pchg_perc=0.05,
        pchg_chg_fc=fake.random_number(digits=2),
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    pcf_obj = quote_schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="1004",
        pchg_type="005",
        pchg_perc=0.25,
        pchg_chg_fc=fake.random_number(digits=2),
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    itl_obj = quote_schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="2004",
        pchg_type="002",
        pchg_perc=0.20,
        pchg_chg_fc=fake.random_number(digits=2),
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    charges_list.append(stamp_duty_obj)
    charges_list.append(pcf_obj)
    charges_list.append(itl_obj)
    return charges_list


def create_covers_list() -> list[quote_schemas.ProposalCoverCreate]:
    """

    @rtype: object
    """
    covers_list = []
    proposal_cover_obj = quote_schemas.ProposalCoverCreate(
        cvr_sr_no=1,
        prc_code="3301",
        prc_rate=1.75,
        prc_rate_per=1000,
        prc_si_curr_code="KES",
        prc_prem_curr_code="KES",
        prc_si_fc=str(fake.random_number(digits=4)),
        prc_prem_fc=str(fake.random_number(digits=6)),
    )
    covers_list.append(proposal_cover_obj)
    return covers_list


def create_smis_list() -> list[quote_schemas.ProposalSMICreate]:
    smis_list = []
    proposal_smi_obj = quote_schemas.ProposalSMICreate(
        smi_sr_no=1,
        prs_smi_code="23001",
        prs_rate=1.75,
        prs_rate_per=1000,
        prs_si_fc=str(fake.random_number(digits=6)),
        prs_prem_fc=str(fake.random_number(digits=4)),
        prs_smi_desc="Finished Products",
    )
    smis_list.append(proposal_smi_obj)
    return smis_list


def create_risks_list(
        covers_list: list[quote_schemas.ProposalCoverCreate],
        smis_list: list[quote_schemas.ProposalSMICreate],
) -> list[quote_schemas.ProposalRiskCreate]:
    risks_list = []
    flexi_dict = {"transit_type": {"prai_code_07": random.choice(['AIR', 'SEA', 'ROAD'])},
                  "goods_desc": {"prai_remarks_06": fake.catch_phrase()},
                  "vessel_name": {"prai_data_04": fake.domain_word()},
                  "port_from_code": {"prai_code_02": fake.credit_card_security_code()},
                  "port_to_code": {"prai_code_08": fake.credit_card_security_code()},
                  "final_dest": {"prai_data_01": fake.city()},
                  "voyage_desc": {"prai_data_05": fake.sentence()},
                  "cargo_value": {"prai_num_01": str(fake.random_number(digits=6))},
                  "shipment_mode_code": {"prai_code_01": fake.credit_card_security_code()},
                  "valuation_basis_code": {"prai_code_04": "001"},
                  "shipment_si": {"prai_num_07": str(fake.random_number(digits=6))},
                  "cargo_type_code": {"prai_code_03": fake.credit_card_security_code()},
                  "idf_number": {"prai_data_06": fake.word()}}
    proposal_risk_obj = quote_schemas.ProposalRiskCreate(
        risk_sr_no=1,
        prai_flexi=flexi_dict,
        proposalcovers=covers_list,
        proposalsmis=smis_list,
    )
    risks_list.append(proposal_risk_obj)
    return risks_list


def create_sections_list(
        risks_list: list[quote_schemas.ProposalRiskCreate],
) -> list[quote_schemas.ProposalSectionCreate]:
    sections_list = []
    proposal_section_obj = quote_schemas.ProposalSectionCreate(
        sec_sr_no=1, psec_sec_code="300302", proposalrisks=risks_list
    )
    sections_list.append(proposal_section_obj)
    return sections_list


def create_proposals_list(
        sections_list: list[quote_schemas.ProposalSectionCreate],
        charges_list: list[quote_schemas.ProposalChargeCreate],
) -> list[quote_schemas.ProposalCreate]:
    proposals_list = []
    proposal_obj = quote_schemas.ProposalCreate(
        prop_sr_no=1,
        prop_paymt_ref=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        prop_paymt_date=fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S"),
        pol_quot_no=str(fake.random_number(digits=10)),
        pol_comp_code="001",
        pol_divn_code="101",
        pol_dept_code="30",
        pol_prod_code="3001",
        pol_type="5006",
        pol_cust_code="200396",
        pol_assr_code="K99999999",
        pol_fm_dt=fake.date_time_this_year(),
        pol_to_dt=fake.date_time_this_year(),
        pol_prem_curr_code="KES",
        pol_dflt_si_curr_code="KES",
        proposalsections=sections_list,
        proposalcharges=charges_list,
    )
    proposals_list.append(proposal_obj)
    return proposals_list


def create_quote() -> Any:
    covers_list = create_covers_list()
    smis_list = create_smis_list()
    risks_list = create_risks_list(covers_list, smis_list)
    sections_list = create_sections_list(risks_list)
    charges_list = create_charges_list()
    proposals_list = create_proposals_list(sections_list, charges_list)

    quote = quote_schemas.QuoteCreate(
        quot_ref=''.join(random.choices(string.digits, k=10)),
        quot_paymt_ref=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        quot_paymt_date=fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S"),
        quot_assr_name=fake.name(),
        quot_assr_nic=''.join(random.choices(string.digits, k=7)),
        quot_assr_pin="P" + ''.join(random.choices(string.digits, k=8)) + "Y",
        quot_assr_phone="+2547" + ''.join(random.choices(string.digits, k=8)),
        quot_assr_email=fake.email(),
        proposals=proposals_list,
    )

    return quote


def create_dyn_marine_payload() -> Any:
    marine_quote = vendor_schemas.QuoteMarineCreate(
        Reference=''.join(random.choices(string.digits, k=10)),
        MCI_PaymentStatus="sucess",
        MCI_MPESAReference=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        MCI_MPESAAmount=str(fake.random_number(digits=5)),
        MCI_MPESAPayDate=fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S"),
        MCI_IRAPolicyNum=''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
        MCI_Cargo_ImporterName=fake.name(),
        MCI_Cargo_ImporterAddress=fake.address(),
        MCI_Cargo_ImporterPIN="P" + ''.join(random.choices(string.digits, k=10)) + "Y",
        MCI_AccountType=str(fake.random_number(digits=2)),
        MCI_CustomerType="ClearingAgent",
        MCI_ClearingAgentPIN="A" + ''.join(random.choices(string.digits, k=10)) + "R",
        MCI_ClearingAgentName=fake.name(),
        MCI_CAEmail=fake.email(),
        MCI_InsuranceID=str(fake.random_int(min=3, max=5)),
        MCI_InsuranceName=fake.word() + "Insurance",
        MCI_QuotationAmount=str(fake.random_number(digits=5)),
        MCI_QuotationNumber=str(fake.random_number(digits=4)),
        MCI_QuoteDateTime=str(fake.date_time_this_year().strftime("%Y-%m-%d")),
        MCI_QuoteDateExpiry=str(fake.date_time_this_year().strftime("%Y-%m-%d")),
        MCI_Cargo_IDF=''.join(random.choices(string.ascii_uppercase + string.digits, k=15)),
        MCI_Cargo_HS_Codes=str(fake.random_number(digits=8)),
        MCI_Cargo_Description=fake.catch_phrase(),
        MCI_Cargo_invoiceamount=str(fake.random_number(digits=6)),
        MCI_Cargo_Packingmode="Containerised",
        MCI_Cargo_dischargedate=str(fake.date_time_this_year().strftime("%Y-%m-%d")),
        MCI_Cargo_loadingdate=str(fake.date_time_this_year().strftime("%Y-%m-%d")),
        MCI_Cargo_originport=fake.city(),
        MCI_Cargo_destinationport=fake.city(),
        MCI_Cargo_transhipmentStatus="Y",
        MCI_Cargo_country_origin=fake.country(),
        MCI_Cargo_country_destination=fake.country(),
        MCI_Cargo_ModeofTransport="Sea",
        MCI_Cargo_InsuranceCoverPeriodDays=str(fake.random_number(digits=3)),
        MCI_Vessel_Name=''.join(random.choices(string.ascii_uppercase, k=6))
    )
    marine_quote_json = json.dumps(jsonable_encoder(marine_quote.model_dump(exclude_unset=True)))
    enc_marine_quote_json = aes_encrypt(marine_quote_json)
    return {"MCINotification":enc_marine_quote_json}
