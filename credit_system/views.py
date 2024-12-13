# API Views for Credit System
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from .models import Customer, Loan
from datetime import date
from math import ceil
from decimal import Decimal

@api_view(['POST'])
def register(request):
    data = request.data
    monthly_income = Decimal(data['monthly_income'])  # Convert to Decimal
    customer = Customer.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data['phone_number'],
        monthly_salary=data['monthly_income'],
        age=data['age']
    )
    return Response({
        'customer_id': customer.customer_id,
        'name': f"{customer.first_name} {customer.last_name}",
        'age': customer.age,
        'monthly_income': customer.monthly_salary,
        'approved_limit': customer.approved_limit,
        'phone_number': customer.phone_number
    })

@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    customer = get_object_or_404(Customer, customer_id=data['customer_id'])

    # Calculate credit score (simplified logic for demo purposes)
    loans = Loan.objects.filter(customer=customer)
    total_loans = loans.count()
    on_time_loans = loans.filter(emis_paid_on_time=True).count()
    current_year_loans = loans.filter(start_date__year=date.today().year).count()
    total_volume = sum(loan.loan_amount for loan in loans)
    credit_score = (on_time_loans / total_loans * 50 if total_loans > 0 else 0) + \
                   (current_year_loans * 10) + (min(total_volume, customer.approved_limit) / customer.approved_limit * 40)

    if sum(loan.monthly_repayment for loan in loans) > 0.5 * customer.monthly_salary:
        credit_score = 0

    # Determine eligibility
    approval = credit_score > 50
    interest_rate = data['interest_rate']
    corrected_interest_rate = interest_rate

    if 30 < credit_score <= 50:
        corrected_interest_rate = max(12, interest_rate)
    elif 10 < credit_score <= 30:
        corrected_interest_rate = max(16, interest_rate)
    elif credit_score <= 10:
        approval = False

    return Response({
        'customer_id': customer.customer_id,
        'approval': approval,
        'interest_rate': interest_rate,
        'corrected_interest_rate': corrected_interest_rate,
        'tenure': data['tenure'],
        'monthly_installment': ceil(data['loan_amount'] * corrected_interest_rate / 100 / 12)
    })

@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer = get_object_or_404(Customer, customer_id=data['customer_id'])

    # Check loan feasibility
    if customer.current_debt + data['loan_amount'] > customer.approved_limit:
        return Response({
            'loan_id': None,
            'customer_id': customer.customer_id,
            'loan_approved': False,
            'message': "Loan amount exceeds approved limit.",
            'monthly_installment': 0
        })

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=data['loan_amount'],
        tenure=data['tenure'],
        interest_rate=data['interest_rate'],
        monthly_repayment=ceil(data['loan_amount'] * data['interest_rate'] / 100 / 12),
        start_date=date.today(),
        end_date=date.today().replace(year=date.today().year + data['tenure'] // 12)
    )

    return Response({
        'loan_id': loan.loan_id,
        'customer_id': customer.customer_id,
        'loan_approved': True,
        'message': "Loan approved successfully.",
        'monthly_installment': loan.monthly_repayment
    })

@api_view(['GET'])
def view_loan(request, loan_id):
    loan = get_object_or_404(Loan, loan_id=loan_id)
    customer = loan.customer
    return Response({
        'loan_id': loan.loan_id,
        'customer': {
            'id': customer.customer_id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'phone_number': customer.phone_number,
        },
        'loan_amount': loan.loan_amount,
        'interest_rate': loan.interest_rate,
        'monthly_installment': loan.monthly_repayment,
        'tenure': loan.tenure
    })

@api_view(['GET'])
def view_loans(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = customer.loans.all()
    return Response([
        {
            'loan_id': loan.loan_id,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_repayment,
            'repayments_left': max(0, loan.tenure - ((date.today() - loan.start_date).days // 30))
        } for loan in loans
    ])

def home_page(request):
    return render(request, 'home.html')