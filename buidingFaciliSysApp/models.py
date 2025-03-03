from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

class CustomUser(AbstractUser):
    userType = models.CharField(blank=True,max_length=10)

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    update_cou = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def update(self, name, email, phone, address, city, state, zip):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.update_cou += 1
        self.last_update = datetime.now()
        self.save()


class Contractor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    proof = models.FileField(upload_to='proofs/', null=True)
    update_cou = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def update(self, name, email, phone, address, city, state, zip):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.update_cou += 1
        self.last_update = datetime.now()
        self.save()
    

class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    proof = models.FileField(upload_to='proofs/', null=True)
    update_cou = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def update(self, name, email, phone, address, city, state, zip):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.update_cou += 1
        self.last_update = datetime.now()
        self.save()
    
    
class Customer_request(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    request = models.TextField()
    request_date = models.DateTimeField(auto_now=True)
    request_status = models.BooleanField(default=False)
    amount = models.FloatField(null=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.request

    def update_request(self, request):
        self.request = request
        self.save()
    
    def update_request_status(self):
        self.request_status = True
        self.save()
    
    def update_payment_status(self):
        self.payment_status = True
        self.save()

class Worker_allocation(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    customer_request = models.ForeignKey(Customer_request, on_delete=models.CASCADE)
    allocation_date = models.DateTimeField(auto_now=True)
    allocation_status = models.BooleanField(default=False)
    work_status = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.worker.name

    def update_allocation_status(self):
        self.allocation_status = True
        self.save()
    
    def update_work_status(self):
        self.work_status = True
        self.save()
    
    def update_payment_status(self):
        self.payment_status = True
        self.save()

class Request_feedback(models.Model):
    Customer_request = models.ForeignKey(Customer_request, on_delete=models.CASCADE,null=True)
    feedback = models.TextField()
    feedback_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feedback

    def update_feedback(self, feedback):
        self.feedback = feedback
        self.save()

class payment_of_worker(models.Model):
    worker_allocation = models.ForeignKey(Worker_allocation, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()

    def __str__(self):
        return self.worker_allocation.worker.name

    def update_payment_status(self):
        self.payment_status = True
        self.save()

class payment_of_contractor(models.Model):
    customer_req = models.ForeignKey(Customer_request, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()

    def __str__(self):
        return self.customer_req.contractor.name

    def update_payment_status(self):
        self.payment_status = True
        self.save()

