import fastapi
from fastapi import Depends, HTTPException
from sqlmodel import Session, select, func, or_

import datetime
from datetime import timedelta
import calendar

from app.models.models import OnlineApplication, Loan, Repayment, LoanDetail, Accounts

from app.database.db import get_session
from app.security import bearer

router = fastapi.APIRouter()

def get_start_end_date(option):
    today = datetime.date.today()
    if option == 'today':
        start_date = end_date = today
    
    elif option == 'week':
        week_of_day = today.weekday()
        start_date = today - timedelta(days = week_of_day)
        end_date = today + timedelta(days = 6 - week_of_day)
    
    elif option == 'month':
        year = today.year
        month = today.month
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    
    elif option == 'year':
        start_date = datetime.date(today.year, 1, 1)
        end_date = datetime.date(today.year, 12, 31)
   
    return start_date, end_date


@router.get(
    '/applicationsummary/{option}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Dashboard"],
    include_in_schema=True,
    description="Dashboard-Appication Summary",
)
def get_application_summary(option: str, session: Session= Depends(get_session)):
    start_date = end_date = ''
    if option != 'all':
        start_date, end_date = get_start_end_date(option)

    query_total_application = select(OnlineApplication).where(
        OnlineApplication.hidden == 0,
        OnlineApplication.application_date >= start_date,
        OnlineApplication.application_date <= end_date
    )
    total_application_count = len(session.exec(query_total_application).all())

    query_pending_application = select(OnlineApplication).where(
        OnlineApplication.hidden == 0,
        OnlineApplication.application_date >= start_date,
        OnlineApplication.application_date <= end_date,
        OnlineApplication.status == 0
    )
    pending_application_count = len(session.exec(query_pending_application).all())

    query_approved_application = select(OnlineApplication).where(
        OnlineApplication.hidden == 0,
        OnlineApplication.application_date >= start_date,
        OnlineApplication.application_date <= end_date,
        OnlineApplication.status == 1
    )
    approved_application_count = len(session.exec(query_approved_application).all())

    query_rejected_application = select(OnlineApplication).where(
        OnlineApplication.hidden == 0,
        OnlineApplication.application_date >= start_date,
        OnlineApplication.application_date <= end_date,
        OnlineApplication.status == 2
    )
    rejected_application_count = len(session.exec(query_rejected_application).all())
    
    return {
        'total_application': total_application_count,
        'pending_application': pending_application_count,
        'approved_application': approved_application_count,
        'rejected_application': rejected_application_count
    }

@router.get(
    '/totalsummary/{option}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Dashboard"],
    include_in_schema=True,
    description="Dashboard-Total Summary",
)
def get_total_summary(option: str, session: Session= Depends(get_session)):
    start_date, end_date = get_start_end_date(option)
    query_loan = select(func.sum((func.abs(Loan.loanamount))), func.count(Loan.loanid)).where(
        Loan.hidden == 0,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date
    )
    total_loan_amount, loan_count = session.exec(query_loan).first()
    if total_loan_amount == None:
        total_loan_amount = 0

    # Income
    query_repayment = select(func.sum(Repayment.actualrepayamount)).where(
        Repayment.hidden == 0,
        Repayment.actualrepaydate >= start_date,
        Repayment.actualrepaydate <= end_date,
        Repayment.actualrepaydate != None,
    )
    total_repayment_amount = session.exec(query_repayment).first()
    if total_repayment_amount == None:
        total_repayment_amount = 0

    query_credit = select(func.sum(Accounts.amount)).where(
        Accounts.hidden == 0,
        Accounts.transactiondate >= start_date,
        Accounts.transactiondate <= end_date,
        Accounts.transaction == 'Credit'.upper()
    )
    total_credit_amount = session.exec(query_credit).first()
    if total_credit_amount == None:
        total_credit_amount = 0

    query_transfer = select(func.sum(Accounts.amount)).where(
        Accounts.hidden == 0,
        Accounts.transactiondate >= start_date,
        Accounts.transactiondate <= end_date,
        Accounts.transaction == 'Transfer In'.upper()
    )
    total_transfer_amount = session.exec(query_transfer).first()
    if total_transfer_amount == None:
        total_transfer_amount = 0

    total_income = total_repayment_amount + total_credit_amount + total_transfer_amount

    # Expense
    query_debit = select(func.sum(Accounts.amount)).where(
        Accounts.hidden == 0,
        Accounts.transactiondate >= start_date,
        Accounts.transactiondate <= end_date,
        Accounts.transaction == 'Debit'
    )
    total_debit_amount = session.exec(query_debit).first()
    if total_debit_amount == None:
        total_debit_amount = 0

    query_transfer_out = select(func.sum(Accounts.amount)).where(
        Accounts.hidden == 0,
        Accounts.transactiondate >= start_date,
        Accounts.transactiondate <= end_date,
        Accounts.transaction == 'Transfer Out'.upper()
    )
    total_transfer_out_amount = session.exec(query_transfer_out).first()
    if total_transfer_out_amount == None:
        total_transfer_out_amount = 0

    total_expense = total_loan_amount + total_debit_amount + total_transfer_out_amount

    total_growth = total_income - total_expense

    return {
        'total_sales': loan_count,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_growth': total_growth
    }

@router.get(
    '/loansummary/{option}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Dashboard"],
    include_in_schema=True,
    description="Dashboard-Loan Summary",
)
def get_loan_summary(option: str, session: Session= Depends(get_session)):
    start_date, end_date = get_start_end_date(option)

    query_loan = select(func.sum((func.abs(Loan.loanamount))), func.count(Loan.loanid)).where(
        Loan.hidden == 0,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date,        
    )
    total_loan_amount, loan_count = session.exec(query_loan).first()

    query_repayment = select(func.sum(Repayment.principal), func.sum(Repayment.interest + Repayment.late_interest), func.sum(Repayment.otherpermit + Repayment.late_fee)).where(
        Repayment.hidden == 0,
        Repayment.actualrepaydate >= start_date,
        Repayment.actualrepaydate <= end_date,
        Repayment.actualrepaydate != None,
    )
    principal_amount, interest_amount, other_permit_amount = session.exec(query_repayment).first()

    return {
        'total_loan': total_loan_amount,
        'loan_count': loan_count,
        'principal_amount': principal_amount,
        'interest_amount': interest_amount,
        'other_permit_amount': other_permit_amount
    }

@router.get(
    '/foreignersummary/{option}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Dashboard"],
    include_in_schema=True,
    description="Dashboard-Foreigner Summary",
)
def get_foreigner_summary(option: str, session: Session= Depends(get_session)):
    start_date, end_date = get_start_end_date(option)

    query_total_foreinger = select(func.abs(func.sum(Loan.loanamount)), func.count(Loan.id)).where(
        Loan.loanid == LoanDetail.loanid,
        Loan.hidden == 0,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date,
        LoanDetail.incomepa <= 5000,
        or_(LoanDetail.nric.like('F%'), LoanDetail.nric.like('G%')),
    )
    get_total_foreigner = session.exec(query_total_foreinger).all()
    get_total_foreigner_amount = 0
    for amount in get_total_foreigner:
        if amount[0] != None:
            get_total_foreigner_amount += amount[0]

    query_foreigner = select(func.abs(func.sum(Loan.loanamount)), func.count(Loan.id)).where(
        Loan.loanid == LoanDetail.loanid,
        Loan.hidden == 0,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date,
        LoanDetail.incomepa <= 5000,
        or_(LoanDetail.nric.like('F%'), LoanDetail.nric.like('G%')),
        or_(Loan.IsDCL == None, Loan.IsDCL == 0),
        Loan.outstanding_principal > 0
    ).group_by(LoanDetail.nric)

    foreiger_amount = session.exec(query_foreigner).all()
    total_foreigner = 0
    for amount in foreiger_amount:
        if amount[0] is not None:            
            total_foreigner += amount[0]

    query_foreigner_unique = select(func.abs(func.sum(Loan.loanamount)), func.count(Loan.id)).where(
        Loan.loanid == LoanDetail.loanid,
        Loan.hidden == 0,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date,
        LoanDetail.incomepa <= 5000,
        or_(LoanDetail.nric.like('F%'), LoanDetail.nric.like('G%')),
        or_(Loan.IsDCL == None, Loan.IsDCL == 0),
    ).group_by(LoanDetail.nric)

    foreiger_unique = session.exec(query_foreigner_unique).all()
    total_foreigner_unique = 0
    for unique in foreiger_unique:
        if unique[0] is not None:            
            total_foreigner_unique += unique[0]

    query_total_foreinger_paid = select(func.abs(func.sum(Loan.loanamount)), func.count(Loan.id)).where(
        Loan.loanid == Repayment.loanid,
        Loan.loanid == LoanDetail.loanid,
        Loan.hidden == 0,
        Repayment.hidden == 0,
        Repayment.actualrepaydate != None,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date,
        LoanDetail.incomepa <= 5000,
        or_(LoanDetail.nric.like('F%'), LoanDetail.nric.like('G%')),
    )
    total_foreigner_paid = session.exec(query_total_foreinger_paid).all()
    total_foreigner_paid_amount = 0
    for amount in total_foreigner_paid:
        if amount[0] is not None:            
            total_foreigner_paid_amount += amount[0]

    return {
        'foreigner_date': str(datetime.date.today()),
        'foreigner_limit': 'Max',
        'total_foreigner': total_foreigner,
        'total_foreigner_unique': total_foreigner_unique,
        'total_loan_amount': get_total_foreigner_amount,
        'total_foreigner_balance': total_foreigner - total_foreigner_paid_amount
    }

@router.get(
    '/transactionsummary/{option}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Dashboard"],
    include_in_schema=True,
    description="Dashboard-Transaction Summary",
)
def get_transaction_summary(option: str, session: Session = Depends(get_session)):
    start_date, end_date = get_start_end_date(option)

    query_loan = select(func.sum((func.abs(Loan.loanamount))), func.count(Loan.loanid)).where(
        Loan.hidden == 0,
        Loan.loandate >= start_date,
        Loan.loandate <= end_date,        
    )
    total_loan_amount, loan_count = session.exec(query_loan).first()
    if total_loan_amount == None:
        total_loan_amount = 0

    query_repayment = select(func.sum(Repayment.principal), func.sum(Repayment.interest + Repayment.late_interest), func.sum(Repayment.otherpermit + Repayment.late_fee)).where(
        Repayment.hidden == 0,
        Repayment.actualrepaydate >= start_date,
        Repayment.actualrepaydate <= end_date,
        Repayment.actualrepaydate != None,
    )
    principal_amount, interest_amount, other_permit_amount = session.exec(query_repayment).first()
    if principal_amount == None:
        principal_amount = 0
    if interest_amount == None:
        interest_amount = 0
    if other_permit_amount == None:
        other_permit_amount = 0

    query_credit = select(func.sum(Accounts.amount)).where(
        Accounts.hidden == 0,
        Accounts.transactiondate >= start_date,
        Accounts.transactiondate <= end_date,
        Accounts.transaction == 'Credit'.upper()
    )
    total_credit_amount = session.exec(query_credit).first()
    if total_credit_amount == None:
        total_credit_amount = 0
    
    query_debit = select(func.sum(Accounts.amount)).where(
        Accounts.hidden == 0,
        Accounts.transactiondate >= start_date,
        Accounts.transactiondate <= end_date,
        Accounts.transaction == 'Debit'
    )
    total_debit_amount = session.exec(query_debit).first()
    if total_debit_amount == None:
        total_debit_amount = 0

    return {
        'total_loand': total_loan_amount,
        'total_repayment': principal_amount + interest_amount + other_permit_amount,
        'total_debit': total_debit_amount,
        'total_credit': total_credit_amount
    }

@router.get(
    '/collectionsummary/{option}',
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Dashboard"],
    include_in_schema=True,
    description="Dashboard-Collection Summary",
)
def get_collection_summary(option: str, session: Session = Depends(get_session)):
    start_date, end_date = get_start_end_date(option)

    query_total_collection = select(func.count(Repayment.id).label('total_count'), func.sum(Repayment.repayamount).label('total_amount'), func.sum(Repayment.principal).label('total_principal'), func.sum(Repayment.interest + Repayment.interest).label('total_interest')).where(
        Loan.loanid == Repayment.loanid,
        Loan.loanid == LoanDetail.loanid,
        Repayment.actualrepaydate == None,
        LoanDetail.status == 'BORROWER',
        Repayment.repaydate >= start_date,
        Repayment.repaydate <= end_date,
        LoanDetail.pos == 1,
        Loan.hidden == 0,
        Repayment.hidden == 0
    )

    total_collection = session.exec(query_total_collection).first()

    query_collection_list = select(Loan.id.label('id'), Loan.loanno.label('loanno'), LoanDetail.trans_name.label('name'), LoanDetail.nric.label('nric'), Repayment.repayamount.label('amount'), Repayment.repaydate.label('due_date'), Repayment.remarks.label('remark')).where(
        Loan.loanid == Repayment.loanid,
        Loan.loanid == LoanDetail.loanid,
        Repayment.actualrepaydate == None,
        LoanDetail.status == 'BORROWER',
        Repayment.repaydate >= start_date,
        Repayment.repaydate <= end_date,
        LoanDetail.pos == 1,
        Loan.hidden == 0,
        Repayment.hidden == 0
    )
    collection_list = session.exec(query_collection_list).all()

    return {
        'total_collection_count': total_collection['total_count'],
        'total_collection_amount': total_collection['total_amount'],
        'collection_list': collection_list
    }