from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employees/', views.employees_list_view, name='employees'),
    path('dashboard/employee/', views.employee_view, name='employee'),
    path('dashboard/schedules/', views.schedules_view, name='schedules'),
    path('dashboard/shifts/delete', views.shifts_delete_view, name='shift_delete'),
    path('dashboard/create-schedule/', views.create_schedule_view, name='create_schedule'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"),name='logout'),
]