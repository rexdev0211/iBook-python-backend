from lib2to3.pgen2.token import OP
from optparse import Option
from typing import Optional
from pydantic import condecimal

from sqlalchemy import false
from sqlmodel import Field, SQLModel, UniqueConstraint, Relationship

import datetime

class AccessCompany(SQLModel, table=True):
    """
        AccessCompany Table
    """
    __table_args__ = (UniqueConstraint('id'),)
    id: Optional[int] = Field(default=None, primary_key=True)
    admin: str
    company: str
    alias: int
    name: str
    login: str
    excpaymentmode: str
    password: str
    limiter: Optional[int] = 1
    passwordchange: datetime.datetime = Field(default=datetime.datetime.utcnow())
    loan: int
    profile: int
    journal: int
    account: int
    report: int
    readonly: int
    timelimit: int
    createdate: datetime.datetime = Field(default=datetime.datetime.utcnow())
    ipaddress: str
    createdby: str
    allowrepayedit: int
    domain: str
    employee_id: str
    counter: int
    statusblock: str
    comm: Optional[str] = '0'
    level: str
    team: str
    user1: int
    user2: int
    blockuser: int
    phoneno: Optional[str] = None
    branching: Optional[int] = 0
    openday: Optional[str] = 'MTWHFSU'
    openhour: datetime.time = Field(default='00:00:00')
    closehour: datetime.time = Field(default='23:59:59')
    exctranstype: Optional[str] = '1,1,1,1,1,1,1'
    tnc_read: Optional[int] = 0
    roles: str
    signature: str

class OnlineApplication(SQLModel, table=True):
    """
        OnlineApplication Table
    """
    __table_args__ = (UniqueConstraint('id'),)
    id: Optional[int] = Field(default=None, primary_key=True)
    company: Optional[str] = None
    application_date: datetime.datetime
    amount: condecimal(max_digits=15, decimal_places=2)
    no_of_loan: str
    active_loan: str
    name: str
    ictype: str
    ictype_detail: Optional[str] = None
    ictype_remark: Optional[str] = None
    nric: str
    dob: datetime.datetime
    nationality: str
    gender: str
    martial: str
    email: Optional[str] = None
    phone: Optional[str] = None
    additional_phone: Optional[str] = None
    home_phone: Optional[str] = None
    ownership: Optional[str] = None
    property_type: Optional[str] = None
    is_oversea: Optional[int] = None
    postalcode: Optional[str] = None
    buildingnumber: Optional[str] = None
    unit: Optional[str] = None
    buildingname: Optional[str] = None
    streetname: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    company_name: Optional[str] = None
    company_reg_no: Optional[str] = None
    company_address: str
    company_unit: Optional[str] = None
    company_buildingnumber: Optional[str] = None
    company_buildingname: Optional[str] = None
    company_streetname: Optional[str] = None
    company_postalcode: Optional[str] = None
    company_phone: Optional[str] = None
    position: Optional[str] = None
    job_period: Optional[str] = None
    salary_date: Optional[str] = None
    monthly_salary: condecimal(max_digits=15, decimal_places=2)
    annual_income: condecimal(max_digits=15, decimal_places=2)
    nok_name: Optional[str] = None
    relationship: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_name_2: Optional[str] = None
    relationship_2: Optional[str] = None
    nok_phone_2: Optional[str] = None
    application_source: Optional[str] = None
    source_remark: Optional[str] = None
    status: Optional[int] = 0 # '0=Pending, 1=Active, 2=Reject',
    reject_reason: str
    reject_remark: str
    hidden: Optional[int] = 0
    loanno: Optional[str] = None
    branch: Optional[str] = None
    label_id: Optional[int] = None
    remark: str
    singpass_json: str
    createdate: datetime.datetime
    createdby: Optional[str] = None
    updatedate: Optional[datetime.datetime] = None
    updatedby: Optional[str] = None
    loanid: Optional[str] = None
    loan_id: Optional[int] = None

class Loan(SQLModel, table=True):
    """
        OnlineApplication Table
    """
    __table_args__ = (UniqueConstraint('id'),)
    loanid: datetime.datetime
    id: Optional[int] = Field(default=None, primary_key=True)
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
    loanguarantee: Optional[str] = None
    term: int
    package: str
    outstanding_principal: condecimal(max_digits=10, decimal_places=2) = Field(default=0.00)
    interestratepa: condecimal(max_digits=10, decimal_places=2)
    acceptance: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    applicationfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    statementfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    creditreportfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    processingfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    variationfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    billofsalefee: condecimal(max_digits=10, decimal_places=2) = Field(default=None) # 'Bill Of Sale Preparation',
    guaranteefee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    mortgagefee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    defferedpaymentfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None) # '= due date adjustment fee',
    consolidationfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None) # 'debt consolidation fee',
    renewalfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    laterepaymentfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    lateinterest: condecimal(max_digits=10, decimal_places=2)
    noticemodefee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    demandcostmodefee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    chequedishonourfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    directdishonourfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None) # 'GIRO/Direct dishonour fee',
    legalenforcementfee: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    purposeofloan: str
    loanremark: str
    hidden: int
    createdby: Optional[str] = None
    createdate: datetime.date
    employee_code: str
    advance: str
    laterepaymentperiod: str
    referral: str
    prefixcode: str
    is_company: Optional[int] = 0
    goodwilldiscount: condecimal(max_digits=10, decimal_places=2) = Field(default=None)
    daily: Optional[int] = 0
    period: Optional[str] = '0'
    limit_to: Optional[int] = 200
    isbad_debt: Optional[int] = 0
    earlyredemptionfee: condecimal(max_digits=10, decimal_places=2) = Field(default=0.00)
    termfee: condecimal(max_digits=5, decimal_places=2) = Field(default=0.00)
    zerointerest: condecimal(max_digits=5, decimal_places=2) = Field(default=0.00)
    latefee: condecimal(max_digits=11, decimal_places=2) = Field(default=0.00)
    latefeeperiod: Optional[str] =  'Per Occasion'
    duedateperiod: Optional[str] = None
    variationplan: Optional[int] = 0
    var_term: Optional[int] = 0
    var_package: Optional[str] = None
    var_date: Optional[datetime.date] = None
    onetimepayment: condecimal(max_digits=8, decimal_places=2)
    var_interest: condecimal(max_digits=8, decimal_places=2)
    var_firstrepayment: Optional[datetime.date] = None
    owner: str
    var_signdate: Optional[datetime.date] = None
    editVariationValue: condecimal(max_digits=5, decimal_places=2) = Field(default=0.01)
    loan_app_no: Optional[str] = None
    loan_type: Optional[str] = None
    post_lod: Optional[int] = 0
    post_hys: Optional[int] = 0
    hcs: Optional[int] = 0 # 'hard copy scrapped',
    IsDCL: Optional[int] = 0
    branch: Optional[str] = None
    demand_status: Optional[str] = None
    mlcb_report: Optional[str] = None

class Repayment(SQLModel, table=True):
    """
        OnlineApplication Table
    """
    __table_args__ = (UniqueConstraint('id'),)
    loanid: datetime.datetime
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    repaydate: datetime.date
    actualrepaydate: datetime.date
    repayamount: condecimal(max_digits=10, decimal_places=2)
    actualrepayamount: condecimal(max_digits=10, decimal_places=2)
    paymentmode: str
    principal: condecimal(max_digits=10, decimal_places=2)
    interest: condecimal(max_digits=10, decimal_places=2)
    overdue_interest: condecimal(max_digits=10, decimal_places=2) = Field(default = 0.00)
    late_interest: condecimal(max_digits=10, decimal_places=2) = Field(default = 0.00)
    overdue_late_interest: condecimal(max_digits=10, decimal_places=2) = Field(default = 0.00)
    late_fee: condecimal(max_digits=10, decimal_places=2) = Field(default = 0.00)
    overdue_late_fee: condecimal(max_digits=10, decimal_places=2) = Field(default = 0.00)
    otherpermit: condecimal(max_digits=10, decimal_places=2)
    overdue: condecimal(max_digits=10, decimal_places=2) = Field(default = 0.00)
    receiptno: Optional[str] = ''
    remarks: str
    ledgercode: str
    createdate: datetime.datetime
    createdby: str
    hidden: int
    lateinterest: condecimal(max_digits=10, decimal_places=2)
    interest_occassion: condecimal(max_digits=10, decimal_places=2)
    callingremarks: str
    paid_by: Optional[str] = 'Borrower'
    payer_name: str
    payer_id: Optional[str] = None
    payer_address: str
    payer_contact: Optional[str] = None
    reference_no: Optional[str] = None
    mode_of_payment: Optional[str] = None
    email_notification: Optional[int] = 0
    approval: Optional[int] = 0
    receiver_id: Optional[int] = None

class LoanDetail(SQLModel, table=True):
    """
        LoanDetail Table
    """
    __table_args__ = (UniqueConstraint('id'),)
    loanid: datetime.datetime
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    nric: str
    trans_name: str
    pos: int
    status: str
    address_label: str = Field(default='Address[1]')
    is_overseas: int = Field(default=0)
    postalcode: str
    buildingnumber: str
    unit: str
    streetname: Optional[str] = None
    buildingname: Optional[str] = None
    fulladdress: Optional[str] = None
    address_country: str = Field(default='SGP')
    number_label: str = Field(default='Contact[1]')
    number_code: str = Field(default='65')
    number: str
    number_ext: Optional[str] = None
    incomepa: int
    bankaccount: Optional[str] = None
    bankcode: Optional[str] = None
    liabilities: Optional[str] = None
    liabilities_detail: Optional[str] = None
    firmname: str
    firmreg: Optional[str] = None
    jobperiod: Optional[str] = None
    typeofentities: Optional[str] = None
    basicemployment: Optional[str] = None
    typeofbusiness: Optional[str] = None
    jobtitle: Optional[str] = None
    firmpostalcode: Optional[str] = None
    firmis_overseas: int = Field(default=0)
    firmbuildingnumber: Optional[str] = None
    firmunit: Optional[str] = None
    firmaddress: str
    firmstreetname: Optional[str] = None
    firmbuildingname: Optional[str] = None
    firmaddresscountry: Optional[str] = None
    createdby: str
    createdate: datetime.date
    hidden: str = Field(default='SGP')
    borrower_consent: int = Field(default=0)
    ictype: Optional[str] = None
    nationality: Optional[str] = None
    is_pr: int = Field(default=0)
    dob: datetime.date = Field(default=None)
    biztype: Optional[str] = None
    bankruptcy: int
    bankruptreason: Optional[str] = None
    email: Optional[str] = None
    marital: Optional[str] = None
    languages: Optional[str] = None
    gender: Optional[str] = None
    ethnic: Optional[str] = None
    consent: int
    income_1: str
    income_2: str
    income_3: str
    income_6: str
    income_doc: Optional[str] = None
    description: str
    add_nric: Optional[str] = None
    add_nationality: Optional[str] = None
    add_ictype: Optional[str] = None
    add_is_pr: int
    add_name: Optional[str] = None
    add_acra_pos: Optional[str] = None
    add_is_overseas: int
    add_postalcode: Optional[str] = None
    add_buildingnumber: Optional[str] = None
    add_unit: Optional[str] = None
    add_streetname: Optional[str] = None
    add_buildingname: Optional[str] = None
    add_fulladdress: Optional[str] = None
    add_address_country: str = Field(default='SGP')
    order_id: Optional[str] = None

class Accounts(SQLModel, table=True):
    """
        Accounts Table
    """
    __table_args__ = (UniqueConstraint('id'),)
    id: Optional[int] = Field(default=None, primary_key=True)
    account: str
    amount: condecimal(max_digits=10, decimal_places=2)
    voucherno: str
    chequeno: str
    transactiondate: datetime.date
    transaction: str
    payer: str
    ledgercode: str = Field(default = '')
    description: str
    type_of_pay: str
    remarks: str
    company: str
    createdby: str
    hidden: int
    createdate: datetime.datetime = Field(default=None)
    approval: int = Field(default=0)
    loanid: datetime.datetime = Field(default=None)
    user_signature: int

class Branch(SQLModel, table=True):
    """
        Branch Table
    """
    __table_args__ = (UniqueConstraint('id'), UniqueConstraint('name'), )
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default='')
    company: str = Field(default='')
    color: str = Field(default=None)
    full_address: str = Field(default='0')
    phone_number: str = Field(default='0')
    is_active: Optional[int] = 1

class mlcb_country(SQLModel, table=True):
    """
        mlcb_country Table
    """
    __table_args__ = (UniqueConstraint('id'), )
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    country: str

class sys_label(SQLModel, table=True):
    """
        sys_label Table
    """
    __table_args__ = (UniqueConstraint('id'), )
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    code: str = Field(default=None)
    color: str = Field(default=None)
    status: int = Field(default=None)
    order: int = Field(default=None)
    createdate: datetime.datetime = Field(default=None)
    createdby: str = Field(default=None)
    updatedate: datetime.datetime = Field(default=None)
    updatedby: str = Field(default=None)

