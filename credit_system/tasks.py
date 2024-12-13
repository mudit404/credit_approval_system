import os
from django.conf import settings  # Import settings to access BASE_DIR
from celery import shared_task
import pandas as pd
from .models import Customer, Loan

file_path_cd = os.path.join(settings.BASE_DIR, 'customer_data.xlsx')
file_path_ld = os.path.join(settings.BASE_DIR, 'loan_data.xlsx')

@shared_task
def ingest_customer_data(file_path_cd):
    # Read the customer data from the provided file path
    df = pd.read_excel(file_path_cd)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            phone_number=row['phone_number'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'monthly_salary': row['monthly_salary'],
                'age': row['age'],
                'current_debt': row['current_debt']
            }
        )

@shared_task
def ingest_loan_data(file_path_ld):
    # Read the loan data from the provided file path
    df = pd.read_excel(file_path_ld)
    for _, row in df.iterrows():
        customer = Customer.objects.get(customer_id=row['customer_id'])
        Loan.objects.update_or_create(
            loan_id=row['loan_id'],
            defaults={
                'customer': customer,
                'loan_amount': row['loan_amount'],
                'tenure': row['tenure'],
                'interest_rate': row['interest_rate'],
                'monthly_repayment': row['monthly_repayment'],
                'emis_paid_on_time': row['EMIs_paid_on_time'],
                'start_date': row['start_date'],
                'end_date': row['end_date']
            }
        )
