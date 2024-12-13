from django.core.management.base import BaseCommand
from django.conf import settings
import os
import pandas as pd
from credit_system.models import Customer, Loan

class Command(BaseCommand):
    help = 'Manually ingests customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        # Define the file paths
        customer_file_path = os.path.join(settings.BASE_DIR, 'customer_data.xlsx')  # Adjust if needed
        loan_file_path = os.path.join(settings.BASE_DIR, 'loan_data.xlsx')  # Adjust if needed

        # Check if the customer data file exists
        if not os.path.exists(customer_file_path):
            self.stdout.write(self.style.ERROR(f"Customer data file not found at {customer_file_path}"))
            return
        if not os.path.exists(loan_file_path):
            self.stdout.write(self.style.ERROR(f"Loan data file not found at {loan_file_path}"))
            return

        # Ingest customer data
        self.stdout.write(self.style.SUCCESS(f"Processing customer data from {customer_file_path}..."))
        self.ingest_customer_data(customer_file_path)

        # Ingest loan data
        self.stdout.write(self.style.SUCCESS(f"Processing loan data from {loan_file_path}..."))
        self.ingest_loan_data(loan_file_path)

        self.stdout.write(self.style.SUCCESS('Data ingestion tasks have been completed.'))

    def ingest_customer_data(self, file_path):
        # Read the customer data from the provided file path
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'phone_number':row['Phone Number'],
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'monthly_salary': row['Monthly Salary'],
                    'age': row['Age'],
                }
            )

    def ingest_loan_data(self, file_path):
        # Read the loan data from the provided file path
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            try:
                # Retrieve the Customer instance by customer_id
                customer = Customer.objects.get(customer_id=row['Customer ID'])
                
                # Create or update the Loan entry with the corresponding Customer instance
                Loan.objects.update_or_create(
                    loan_id=row['Loan ID'],
                    defaults={
                        'customer': customer,  # Assigning the actual Customer instance
                        'loan_amount': row['Loan Amount'],
                        'tenure': row['Tenure'],
                        'interest_rate': row['Interest Rate'],
                        'monthly_repayment': row['Monthly payment'],
                        'emis_paid_on_time': row['EMIs paid on Time'],
                        'start_date': row['Date of Approval'],
                        'end_date': row['End Date']
                    }
                )
            except Customer.DoesNotExist:
                # Handle case where the Customer with the given ID doesn't exist
                self.stdout.write(self.style.ERROR(f"Customer with ID {row['Customer ID']} not found."))

