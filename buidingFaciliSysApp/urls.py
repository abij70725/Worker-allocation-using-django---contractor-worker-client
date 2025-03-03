from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name=''),
    path('log_in', views.log_in, name='login'),
    path('logout', views.logout, name='logout'),
    path('public_reg', views.public_reg, name='public_reg'),
    path('contractor_reg', views.contractor_reg, name='contractor_reg'),
    path('contractor_add_worker', views.contractor_add_worker, name='contractor_add_worker'),

    path('admin_home', views.admin_home, name='admin_home'),
    path('contractor_home', views.contractor_home, name='contractor_home'),
    path('worker_home', views.worker_home, name='worker_home'),
    path('public_home', views.public_home, name='public_home'),

    path('admin_vw_public', views.admin_vw_public, name='admin_vw_public'),
    path('admin_vw_contractors', views.admin_vw_contractors, name='admin_vw_contractors'),
    path('admin_vw_workers', views.admin_vw_workers, name='admin_vw_workers'),
    path('admin_approve', views.admin_approve, name='admin_approve'),
    path('admin_reject', views.admin_reject, name='admin_reject'),
    path('admin_vw_contractor_reviews', views.admin_vw_contractor_reviews, name='admin_vw_contractor_reviews'),
    
    path('contractor_vw_workers', views.contractor_vw_workers, name='contractor_vw_workers'),
    path('contractor_vw_requests', views.contractor_vw_requests, name='contractor_vw_requests'),
    path('contractor_approve', views.contractor_approve, name='contractor_approve'),
    path('Contractor_vw_requests_more', views.Contractor_vw_requests_more, name='Contractor_vw_requests_more'),
    path('contractor_allocate_worker', views.contractor_allocate_worker, name='contractor_allocate_worker'),
    path('contractor_vw_worker_works', views.contractor_vw_worker_works, name='contractor_vw_worker_works'),
    path('contractor_pay_worker', views.contractor_pay_worker, name='contractor_pay_worker'),
    path('contractor_vw_debits', views.contractor_vw_debits, name='contractor_vw_debits'),
    path('contractor_vw_credits', views.contractor_vw_credits, name='contractor_vw_credits'),

    path('public_vw_contractors', views.public_vw_contractors, name='public_vw_contractors'),
    path('public_vw_contractor_more', views.public_vw_contractor_more, name='public_vw_contractor_more'),
    path('public_vw_my_requests', views.public_vw_my_requests, name='public_vw_my_requests'),
    path('public_vw_req_more', views.public_vw_req_more, name='public_vw_req_more'),
    path('public_pay_contractor', views.public_pay_contractor, name='public_pay_contractor'),
    path('public_vw_my_payments', views.public_vw_my_payments, name='public_vw_my_payments'),

    path('worker_vw_works', views.worker_vw_works, name='worker_vw_works'),
    path('worker_mark_completed', views.worker_mark_completed, name='worker_mark_completed'),
    path('worker_vw_payments', views.worker_vw_payments, name='worker_vw_payments'),
]