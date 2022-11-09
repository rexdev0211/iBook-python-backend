from pydantic import BaseModel, condecimal
from typing import List, Union

import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class PageParam(BaseModel):
    offset: int
    limit: int

class AccessCompanyModel(BaseModel):
    """
        AccessCompany Model
    """
    admin: str
    company: str
    alias: int
    name: str
    login: str
    excpaymentmode: str
    password: str
    limiter: int
    passwordchange: datetime.datetime
    loan: int
    profile: int
    journal: int
    account: int
    report: int
    readonly: int
    timelimit: int
    createdate: datetime.datetime
    ipaddress: str
    createdby: str
    allowrepayedit: int
    domain: str
    employee_id: str
    counter: int
    statusblock: str
    comm: str
    level: str
    team: str
    user1: int
    user2: int
    blockuser: int
    phoneno: str
    branching: int
    openday: str
    openhour: datetime.time
    closehour: datetime.time
    exctranstype: str
    tnc_read: int
    roles: str
    signature: str

class OnlineApplicationModel(BaseModel):
    """
        OnlineApplication Model
    """
    company: str
    application_date: datetime.datetime
    amount: condecimal(max_digits=15, decimal_places=2)
    no_of_loan: str
    active_loan: str
    name: str
    ictype: str
    ictype_detail: str
    ictype_remark: str
    nric: str
    dob: datetime.datetime
    nationality: str
    gender: str
    martial: str
    email: str
    phone: str
    additional_phone: str
    home_phone: str
    ownership: str
    property_type: str
    is_oversea: int
    postalcode: str
    buildingnumber: str
    unit: str
    buildingname: str
    streetname: str
    address: str
    country: str
    company_name: str
    company_reg_no: str
    company_address: str
    company_unit: str
    company_buildingnumber: str
    company_buildingname: str
    company_streetname: str
    company_postalcode: str
    company_phone: str
    position: str
    job_period: str
    salary_date: str
    monthly_salary: condecimal(max_digits=15, decimal_places=2)
    annual_income: condecimal(max_digits=15, decimal_places=2)
    nok_name: str
    relationship: str
    nok_phone: str
    nok_name_2: str
    relationship_2: str
    nok_phone_2: str
    application_source: str
    source_remark: str
    status: int # '0=Pending, 1=Active, 2=Reject',
    reject_reason: str
    reject_remark: str
    hidden: int
    loanno: str
    branch: str
    label_id: int
    remark: str
    singpass_json: str
    createdate: datetime.datetime
    createdby: str
    updatedate: datetime.datetime
    updatedby: str
    loanid: str
    loan_id: int

class LoanModel(BaseModel):
    """
        LoanModel
    """
    loanid: datetime.datetime
    company: str
    loanno: str
    loanamount: int
    agentcode: str
    paymentmode: str
    voucherno: str
    chequeno: str
    loandate: datetime.date
    repaymentdate: datetime.date
    firstrepaymentdate: datetime.date
    typeofloan: str
    loanguarantee: str
    term: int
    package: str
    outstanding_principal: condecimal(max_digits=10, decimal_places=2)
    interestratepa: condecimal(max_digits=10, decimal_places=2)
    acceptance: condecimal(max_digits=10, decimal_places=2)
    applicationfee: condecimal(max_digits=10, decimal_places=2)
    statementfee: condecimal(max_digits=10, decimal_places=2)
    creditreportfee: condecimal(max_digits=10, decimal_places=2)
    processingfee: condecimal(max_digits=10, decimal_places=2)
    variationfee: condecimal(max_digits=10, decimal_places=2)
    billofsalefee: condecimal(max_digits=10, decimal_places=2) # 'Bill Of Sale Preparation',
    guaranteefee: condecimal(max_digits=10, decimal_places=2)
    mortgagefee: condecimal(max_digits=10, decimal_places=2)
    defferedpaymentfee: condecimal(max_digits=10, decimal_places=2) # '= due date adjustment fee',
    consolidationfee: condecimal(max_digits=10, decimal_places=2) # 'debt consolidation fee',
    renewalfee: condecimal(max_digits=10, decimal_places=2)
    laterepaymentfee: condecimal(max_digits=10, decimal_places=2)
    lateinterest: condecimal(max_digits=10, decimal_places=2)
    noticemodefee: condecimal(max_digits=10, decimal_places=2)
    demandcostmodefee: condecimal(max_digits=10, decimal_places=2)
    chequedishonourfee: condecimal(max_digits=10, decimal_places=2)
    directdishonourfee: condecimal(max_digits=10, decimal_places=2) # 'GIRO/Direct dishonour fee',
    legalenforcementfee: condecimal(max_digits=10, decimal_places=2)
    purposeofloan: str
    loanremark: str
    hidden: int
    createdby: str
    createdate: datetime.date
    employee_code: str
    advance: str
    laterepaymentperiod: str
    referral: str
    prefixcode: str
    is_company: int
    goodwilldiscount: condecimal(max_digits=10, decimal_places=2)
    daily: int
    period: str
    limit_to: int
    isbad_debt: int
    earlyredemptionfee: condecimal(max_digits=10, decimal_places=2)
    termfee: condecimal(max_digits=5, decimal_places=2)
    zerointerest: condecimal(max_digits=5, decimal_places=2)
    latefee: condecimal(max_digits=11, decimal_places=2)
    latefeeperiod: str
    duedateperiod: str
    variationplan: int
    var_term: int
    var_package: str
    var_date: datetime.date
    onetimepayment: condecimal(max_digits=8, decimal_places=2)
    var_interest: condecimal(max_digits=8, decimal_places=2)
    var_firstrepayment: datetime.date
    owner: str
    var_signdate: datetime.date
    editVariationValue: condecimal(max_digits=5, decimal_places=2)
    loan_app_no: str
    loan_type: str
    post_lod: int
    post_hys: int
    hcs: int # 'hard copy scrapped',
    IsDCL: int
    branch: str
    demand_status: str
    mlcb_report: str

class RepaymentModel(BaseModel):
    """
        Repayment Model
    """
    loanid: datetime.datetime
    company: str
    repaydate: datetime.date
    actualrepaydate: datetime.date
    repayamount: condecimal(max_digits=10, decimal_places=2)
    actualrepayamount: condecimal(max_digits=10, decimal_places=2)
    paymentmode: str
    principal: condecimal(max_digits=10, decimal_places=2)
    interest: condecimal(max_digits=10, decimal_places=2)
    overdue_interest: condecimal(max_digits=10, decimal_places=2)
    late_interest: condecimal(max_digits=10, decimal_places=2)
    overdue_late_interest: condecimal(max_digits=10, decimal_places=2)
    late_fee: condecimal(max_digits=10, decimal_places=2)
    overdue_late_fee: condecimal(max_digits=10, decimal_places=2)
    otherpermit: condecimal(max_digits=10, decimal_places=2)
    overdue: condecimal(max_digits=10, decimal_places=2)
    receiptno: Union[str, None] = None
    remarks: str
    ledgercode: str
    createdate: datetime.datetime
    createdby: str
    hidden: int
    lateinterest: condecimal(max_digits=10, decimal_places=2)
    interest_occassion: condecimal(max_digits=10, decimal_places=2)
    callingremarks: str
    paid_by: str
    payer_name: str
    payer_id: Union[str, None] = None
    payer_address: str
    payer_contact: Union[str, None] = None
    reference_no: Union[str, None] = None
    mode_of_payment: Union[str, None] = None
    email_notification: Union[int, None] = 0
    approval: Union[int, None] = 0
    receiver_id: Union[int, None] = None

class LoanDetailModel(BaseModel):
    """
        LoanDetail Model
    """
    loanid: datetime.datetime
    company: str
    nric: str
    trans_name: str
    pos: int
    status: str
    address_label: str
    is_overseas: int
    postalcode: str
    buildingnumber: str
    unit: str
    streetname: str
    buildingname: str
    fulladdress: str
    address_country: str
    number_label: str
    number_code: str
    number: str
    number_ext: str
    incomepa: int
    bankaccount: str
    bankcode: str
    liabilities: str
    liabilities_detail: str
    firmname: str
    firmreg: str
    jobperiod: str
    typeofentities: str
    basicemployment: str
    typeofbusiness: str
    jobtitle: str
    firmpostalcode: str
    firmis_overseas: int
    firmbuildingnumber: str
    firmunit: str
    firmaddress: str
    firmstreetname: str
    firmbuildingname: str
    firmaddresscountry: str
    createdby: str
    createdate: datetime.date
    hidden: str
    borrower_consent: int
    ictype: str
    nationality: str
    is_pr: int
    dob: datetime.date
    biztype: str
    bankruptcy: int
    bankruptreason: str
    email: str
    marital: str
    languages: str
    gender: str
    ethnic: str
    consent: int
    income_1: str
    income_2: str
    income_3: str
    income_6: str
    income_doc: str
    description: str
    add_nric: str
    add_nationality: str
    add_ictype: str
    add_is_pr: int
    add_name: str
    add_acra_pos: str
    add_is_overseas: int
    add_postalcode: str
    add_buildingnumber: str
    add_unit: str
    add_streetname: str
    add_buildingname: str
    add_fulladdress: str
    add_address_country: str
    order_id: str

class AccountsModel(BaseModel):
    """
        Accounts Model
    """
    account: str
    amount: condecimal(max_digits=10, decimal_places=2)
    voucherno: str
    chequeno: str
    transactiondate: datetime.date
    transaction: str
    payer: str
    ledgercode: Union[str, None] = None
    description: str
    type_of_pay: str
    remarks: str
    company: str
    createdby: str
    hidden: int
    createdate: Union[datetime.datetime, None] = None
    approval: Union[int, None] = 0
    loanid: Union[datetime.datetime, None] = None
    user_signature: int

class BranchModel(BaseModel):
    """
        Branch Model
    """
    name: str
    company: str
    color: str
    full_address: str
    phone_number: str
    is_active: int

class mlcb_country_model(BaseModel):
    """
        mlcb_country Model
    """
    code: str
    country: str