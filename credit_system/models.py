from django.db import models
from decimal import Decimal

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.IntegerField()
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        self.monthly_salary = Decimal(self.monthly_salary)
        self.approved_limit = round(self.monthly_salary * 36, -5)  # Rounded to the nearest lakh
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer.first_name} {self.customer.last_name}"