import fastapi
from fastapi import Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, Params #, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import Session, select, func, or_

from app.models.models import OnlineApplication, Branch, mlcb_country, sys_label
from app.models.basemodels import OnlineApplicationModel, AccessCompanyModel, PageParam

from app.database.db import get_session
from app.security import bearer

router = fastapi.APIRouter()

def format_address(postalcode, buildingnumber, unit, streetname, buildingname):
    if unit == '':
        fulladdress = buildingnumber + ' ' + streetname + ' ' + buildingname + ' S' + postalcode
    else:
        fulladdress = 'Blk ' + buildingnumber + ' ' + streetname + ' #' + unit + ' ' + buildingname + ' S' + postalcode
    
    return fulladdress

@router.get(
    '/application/get_branches',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Application"],
    include_in_schema=True,
    description="Get Branches from the Company Table",
)
def get_branches_list(current_user: AccessCompanyModel = Depends(bearer.get_current_active_user), session: Session = Depends(get_session)):
    query_branches = select(Branch).where(
        Branch.company == current_user.company
    )
    branch_list = session.exec(query_branches).all()

    return {
        'branch_list': branch_list
    }

@router.get(
    '/application/get_country',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Application"],
    include_in_schema=True,
    description="Get Countries from the mlcb_country Table",
)
def get_country_list(session: Session = Depends(get_session)):
    query_countries = select(mlcb_country)
    country_list = session.exec(query_countries).all()

    return {
        'country_list': country_list
    }

@router.get(
    '/application/get_label_list',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Application"],
    include_in_schema=True,
    description="Get Labels from the sys_label Table",
)
def get_label_list(session: Session = Depends(get_session)):
    query_labels = select(sys_label)
    label_list = session.exec(query_labels).all()

    return {
        'label_list': label_list
    }

@router.post(
    '/application',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Application"],
    include_in_schema=True,
    description="New Application",
)
def create_application(application: OnlineApplicationModel, session: Session= Depends(get_session)):
    if application.ictype.upper() != "FINO":
        application.ictype_detail = ''
        application.ictype_remark = ''
    
    if application.ictype_detail != 'OPASS':
        application.ictype_remark = ''
    
    if application.is_oversea != 1:
        application.address = format_address(application.postalcode, application.buildingnumber, application.unit, application.streetname, application.buildingname)
    
    application.company_address = format_address(application.company_postalcode, application.company_buildingnumber, application.company_unit, application.company_streetname, application.company_buildingname)

    try:
        new_application = OnlineApplication(
            company = application.company,
            application_date = application.application_date,
            amount = application.amount,
            no_of_loan = application.no_of_loan,
            active_loan = application.active_loan,
            name = application.name,
            ictype = application.ictype,
            ictype_detail = application.ictype,
            ictype_remark = application.ictype_remark,
            nric = application.nric,
            dob = application.dob,
            nationality = application.nationality,
            gender = application.gender,
            martial = application.martial,
            email = application.email,
            phone = application.phone,
            additional_phone = application.additional_phone,
            home_phone = application.home_phone,
            ownership = application.ownership,
            property_type = application.property_type,
            address = application.address,
            is_oversea = application.is_oversea,
            unit = application.unit,
            buildingname = application.buildingname,
            buildingnumber = application.buildingnumber,
            streetname = application.streetname,
            postalcode = application.postalcode,
            country = application.country,
            company_name = application.company_name,
            company_reg_no = application.company_reg_no,
            company_address = application.company_address,
            company_unit = application.company_unit,
            company_buildingname = application.company_buildingname,
            company_buildingnumber = application.company_buildingnumber,
            company_streetname = application.company_streetname,
            company_postalcode = application.company_postalcode,
            company_phone = application.company_phone,
            position = application.position,
            job_period = application.job_period,
            salary_date = application.salary_date,
            monthly_salary = application.monthly_salary,
            annual_income = application.annual_income,
            nok_name = application.nok_name,
            relationship = application.relationship,
            nok_phone = application.nok_phone,
            nok_name_2 = application.nok_name_2,
            relationship_2 = application.relationship_2,
            nok_phone_2 = application.nok_phone_2,
            application_source = application.application_source,
            source_remark = application.source_remark,
            status = application.status,
            reject_reason = application.reject_reason,
            reject_remark = application.reject_remark,
            hidden = application.hidden,
            loanno = '',
            branch = application.branch,
            label_id = application.label_id,
            remark = application.remark,
            singpass_json = application.singpass_json,
            createdate = application.createdate,
            createdby = application.createdby,
            updatedate = application.updatedate,
            updatedby = application.updatedby,
            loanid = application.loanid,
            loan_id = application.loan_id
        )
        session.add(new_application)
        session.commit()

        return {
            'response': 'Succeed to create a new application'
        }
    except:
        return {
            'response': 'Failed to create a new application'
        }



@router.get(
    '/application/list/{limit_size}/{offset_size}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Application"],
    include_in_schema=True,
    description="Application List",
    response_model=LimitOffsetPage[OnlineApplicationModel]
)
def get_application_list(limit_size: int, offset_size: int, session: Session = Depends(get_session)):
    if offset_size < 1:
        offset_size = 1
    params = Params(
        page = offset_size,
        size = limit_size
    )

    return paginate(session.query(OnlineApplication), params)

@router.get(
    '/application/search/{limit_size}/{offset_size}/{keyword}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Application"],
    include_in_schema=True,
    description="Application List",
    response_model=LimitOffsetPage[OnlineApplicationModel]
)
def get_application_search(limit_size: int, offset_size: int, keyword: str, session: Session = Depends(get_session)):
    if offset_size < 1:
        offset_size = 1
    params = Params(
        page = offset_size,
        size = limit_size
    )
    
    return paginate(session.query(OnlineApplication).filter(OnlineApplication.name.like(keyword)), params)