from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from django.db.models import Q
from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
                if user.is_superuser == 1:
                    login(request, user)
                    return redirect('/admin_home')
                elif user.userType == 'public':
                    customer = Customer.objects.get(user=user)
                    login(request, user)
                    return redirect('/public_home')
                elif user.userType == 'contractor':
                    contractor = Contractor.objects.get(user=user)
                    login(request, user)
                    return redirect('/contractor_home')
                elif user.userType == 'worker':
                    worker = Worker.objects.get(user=user)
                    login(request, user)
                    return redirect('/worker_home')
                else:
                    messages.error(request, 'No user type found')
        else:
            if CustomUser.objects.filter(username=email).exists():
                if CustomUser.objects.get(username=email).is_active == 0:
                    messages.error(request, 'User not approved or blocked')
                else:
                    messages.error(request, 'Invalid password')
            else:
                messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/log_in')

def public_reg(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = CustomUser.objects.create_user(username=email, password=password, userType='public')
            user.save()
            customer = Customer(user=user, name=request.POST['name'], email=email, phone=request.POST['phone'], address=request.POST['address'], city=request.POST['city'], state=request.POST['state'], zip=request.POST['zip'], password=password)
            customer.save()
            messages.success(request, 'Account created successfully')
            return redirect('/log_in')
    return render(request, 'public_reg.html')

def contractor_reg(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = CustomUser.objects.create_user(username=email, password=password, userType='contractor',is_active=False)
            user.save()
            contractor = Contractor(user=user, name=request.POST['name'], email=email, phone=request.POST['phone'], address=request.POST['address'], city=request.POST['city'], state=request.POST['state'], zip=request.POST['zip'], password=password, proof = request.FILES['proof'])
            contractor.save()
            messages.success(request, 'Account created successfully, wait for admin approval')
            return redirect('/log_in')
    return render(request, 'contractor_reg.html')

def contractor_add_worker(request):
    contractor_id = request.session.get('_auth_user_id')
    contractor = Contractor.objects.get(user_id=contractor_id)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = CustomUser.objects.create_user(username=email, password=password, userType='worker')
            user.save()
            worker = Worker(user=user,contractor = contractor, name=request.POST['name'], email=email, phone=request.POST['phone'], address=request.POST['address'], city=request.POST['city'], state=request.POST['state'], zip=request.POST['zip'], password=password)
            worker.save()
            messages.success(request, 'Worker added successfully')
    return render(request, 'contractor_add_worker.html')

def admin_home(request):
    return render(request, 'admin_home.html')

def contractor_home(request):
    return render(request, 'contractor_home.html')

def worker_home(request):
    return render(request, 'worker_home.html')

def public_home(request):
    return render(request, 'public_home.html')

def admin_vw_public(request):
    publics = Customer.objects.all()
    return render(request, 'admin_vw_public.html', {'publics':publics})

def admin_vw_contractors(request):
    contractors = Contractor.objects.all()
    return render(request, 'admin_vw_contractors.html', {'contractors':contractors})

def admin_vw_workers(request):
    workers = Worker.objects.all()
    return render(request, 'admin_vw_workers.html', {'workers':workers})

def admin_approve(request):
    user_id = request.GET['id']
    returnto = request.GET['return']
    user = CustomUser.objects.get(id=user_id)
    user.is_active = 1
    user.save()
    messages.success(request, 'User approved successfully')
    if returnto == 'public':
        return redirect('/admin_vw_public')
    elif returnto == 'contractor':
        return redirect('/admin_vw_contractors')
    elif returnto == 'worker':
        return redirect('/admin_vw_workers')
    else:
        return redirect('/admin_home')
    
def admin_reject(request):
    user_id = request.GET['id']
    returnto = request.GET['return']
    user = CustomUser.objects.get(id=user_id)
    user.is_active = 0
    user.save()
    messages.success(request, 'User rejected successfully')
    if returnto == 'public':
        return redirect('/admin_vw_public')
    elif returnto == 'contractor':
        return redirect('/admin_vw_contractors')
    elif returnto == 'worker':
        return redirect('/admin_vw_workers')
    else:
        return redirect('/admin_home')
    
def admin_vw_contractor_reviews(request):
    contractor_id = request.GET['id']
    contractor = Contractor.objects.get(user=contractor_id)
    feedbacks = Request_feedback.objects.filter(Customer_request__contractor=contractor)
    return render(request, 'admin_vw_contractor_reviews.html', {'contractor':contractor, 'feedbacks':feedbacks})

def contractor_vw_workers(request):
    workers = Worker.objects.filter(contractor_id=request.session.get('_auth_user_id'))
    return render(request, 'contractor_vw_workers.html', {'workers':workers})

def contractor_vw_requests(request):
    contractor_id = request.session.get('_auth_user_id')
    requests = Customer_request.objects.filter(contractor_id=contractor_id).order_by('-request_date')
    return render(request, 'contractor_vw_requests.html', {'requests':requests})

def contractor_approve(request):
    request_id = request.GET['id']
    to_request = Customer_request.objects.get(id=request_id)
    to_request.update_request_status()
    messages.success(request, 'Request approved successfully')
    return redirect('/contractor_vw_requests')

def Contractor_vw_requests_more(request):
    request_id = request.GET['id']
    print(request_id,"000000000000000000000000000")
    to_request = Customer_request.objects.get(id=request_id)
    workers = Worker.objects.filter(contractor__user=to_request.contractor.user)
    workers_allocated = Worker_allocation.objects.filter(customer_request=to_request)
    return render(request, 'Contractor_vw_requestas_more.html', {'request':to_request, 'workers':workers, 'workers_allocated':workers_allocated})

def contractor_allocate_worker(request):
    request_id = request.GET['rid']
    worker_id = request.GET['wid']
    to_request = Customer_request.objects.get(id=request_id)
    worker = Worker.objects.get(user=worker_id)
    if Worker_allocation.objects.filter(worker=worker, customer_request=to_request).exists():
        messages.error(request, 'Worker already allocated')
        return redirect('/Contractor_vw_requests_more?id='+request_id)
    else:
        to_allocate = Worker_allocation(worker=worker, customer_request=to_request)
        to_allocate.save()
        messages.success(request, 'Worker allocated successfully')
    return redirect('/Contractor_vw_requests_more?id='+request_id)

def contractor_vw_worker_works(request):
    worker_id = request.GET['id']
    worker = Worker.objects.get(user=worker_id)
    works = Worker_allocation.objects.filter(worker=worker)
    return render(request, 'contractor_vw_worker_works.html', {'works':works})

def contractor_pay_worker(request):
    work_id = request.GET['rid']
    if request.method == 'POST':
        amount = request.POST['amount']
        to_work = Worker_allocation.objects.get(id=work_id)
        to_work.update_payment_status()
        payment = payment_of_worker(worker_allocation=to_work, amount=amount)
        payment.save()
        messages.success(request, 'Payment done successfully')
        return redirect('/contractor_vw_worker_works?id='+str(to_work.worker.user.id))
    return render(request, 'contractor_pay_worker.html')

def contractor_vw_debits(request):
    contractor_id = request.session.get('_auth_user_id')
    payments = payment_of_worker.objects.filter(worker_allocation__worker__contractor_id=contractor_id)
    return render(request, 'contractor_vw_debits.html', {'payments':payments})

def contractor_vw_credits(request):
    contractor_id = request.session.get('_auth_user_id')
    payments = payment_of_contractor.objects.filter(customer_req__contractor_id=contractor_id)
    return render(request, 'contractor_vw_credits.html', {'payments':payments})


def public_vw_contractors(request):
    contractors = Contractor.objects.filter(user__is_active=1)
    return render(request, 'public_vw_contractors.html', {'contractors':contractors})

def public_vw_contractor_more(request):
    contractor_id = request.GET['id']
    contractor = Contractor.objects.get(user=contractor_id)
    workers = Worker.objects.filter(contractor_id=contractor_id)
    if request.method == 'POST':
        user_id = request.session.get('_auth_user_id')
        user = CustomUser.objects.get(id=user_id)
        print(user_id,"000000000000000000000000000")
        customer = Customer.objects.get(user=user)
        to_request = Customer_request(user=customer, contractor=contractor, request=request.POST['request'], amount=request.POST['amount'])
        to_request.save()
        messages.success(request, 'Request sent successfully')
        return redirect('/public_vw_my_requests')
    return render(request, 'public_vw_contractor_more.html', {'contractor':contractor, 'workers':workers})

def public_vw_my_requests(request):
    user_id = request.session.get('_auth_user_id')
    user = CustomUser.objects.get(id=user_id)
    customer = Customer.objects.get(user=user_id)
    requests = Customer_request.objects.filter(user=customer).order_by('-request_date')
    return render(request, 'public_vw_my_requests.html', {'requests':requests})

def public_vw_req_more(request):
    request_id = request.GET['id']
    to_request = Customer_request.objects.get(id=request_id)
    workers_allocated = Worker_allocation.objects.filter(customer_request=to_request)
    feedbacks = Request_feedback.objects.filter(Customer_request=to_request).first()
    if request.method == 'POST':
        if feedbacks is not None:
            feedbacks.feedback = request.POST['feedback']
            feedbacks.save()
            messages.success(request, 'Feedback updated successfully')
        else:
            to_feedback = Request_feedback(Customer_request=to_request, feedback=request.POST['feedback'])
            to_feedback.save()
            messages.success(request, 'Feedback added successfully')
        return redirect('/public_vw_req_more?id='+request_id)
    return render(request, 'public_vw_req_more.html', {'request':to_request, 'workers_allocated':workers_allocated, 'feedbacks':feedbacks})    

def public_pay_contractor(request):
    request_id = request.GET['id']
    to_request = Customer_request.objects.get(id=request_id)
    if request.method == 'POST':
        to_request.update_payment_status()
        payment = payment_of_contractor(customer_req=to_request, amount=to_request.amount)
        payment.save()
        messages.success(request, 'Payment done successfully')
        return redirect('/public_vw_req_more?id='+request_id)
    return render(request, 'public_pay_contractor.html',{'amount':to_request.amount})

def public_vw_my_payments(request):
    user_id = request.session.get('_auth_user_id')
    user = CustomUser.objects.get(id=user_id)
    customer = Customer.objects.get(user__id=user_id)
    payments = payment_of_contractor.objects.filter(customer_req__user=customer)
    return render(request, 'public_vw_my_payments.html', {'payments':payments})

def worker_vw_works(request):
    user_id = request.session.get('_auth_user_id')
    worker = Worker.objects.get(user=user_id)
    works = Worker_allocation.objects.filter(worker=worker)
    return render(request, 'worker_vw_works.html', {'works':works})

def worker_mark_completed(request):
    work_id = request.GET['id']
    to_work = Worker_allocation.objects.get(id=work_id)
    to_work.update_work_status()
    messages.success(request, 'Work marked as completed successfully')
    return redirect('/worker_vw_works')

def worker_vw_payments(request):
    user_id = request.session.get('_auth_user_id')
    worker = Worker.objects.get(user=user_id)
    payments = payment_of_worker.objects.filter(worker_allocation__worker=worker)
    return render(request, 'worker_vw_payments.html', {'payments':payments})