from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms.schedule_create_form import ShiftCreationForm, ScheduleCreationForm
from .models import Organization, Schedule, Shift
from .forms.employee_create_form import EmployeeCreationForm, UserCreationForm
from .forms.user_create_form import CustomUserCreationForm
from functools import wraps
import random
from datetime import datetime,timedelta


nav_items = [{ "name":"Dashboard", "link":"" },{ "name": "Employee","link":"employees/"},{ 
     "name":"Schedules", "link":"schedules/"}, {"name":"Time Off","link":"time-off/"},{"name":"Timesheets", "link":"timesheet"},{"name":"Reports","link":"reports"},{"name":"Messages","link":"messages/"},]


COLORS = [{'primary_color': '#FEDAF5', 'secondary_color': '#B60D8B',},{'primary_color': '#E7FFD5', 'secondary_color': '#428B08',},{'primary_color': '#D4FAFF', 'secondary_color': '#0A7584',},{'primary_color': '#CDDDFF', 'secondary_color': '#07328F',},{'primary_color': '#FBDEFF', 'secondary_color': '#6B047A',},{'primary_color': '#FFDCE3', 'secondary_color': '#88001B',},{'primary_color': '#FFCCAD', 'secondary_color': '#983A00',},{'primary_color': '#B3FFE0', 'secondary_color': '#10583A',},{'primary_color': '#EAEDEC', 'secondary_color': '#2A2A2A',},{'primary_color': '#E3D4FF', 'secondary_color': '#4111A2',},{'primary_color': '#C9DDFF', 'secondary_color': '#08295F',},{'primary_color': '#EEFFC5', 'secondary_color': '#5A7810',},{'primary_color': '#FFCBEF', 'secondary_color': '#610B47',},{'primary_color': '#FFF2CC', 'secondary_color': '#856300',},]

def generate_color(color_list):
    return random.choice(color_list)
    

def get_organization(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        try:
            organization = user.admin_of
            kwargs['organization'] = organization
        except Organization.DoesNotExist:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('home')
        else:
            print("'invalid login' error message", user)
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        mutable_post = request.POST.copy()
        mutable_post['email'] = request.POST['username']
        form = CustomUserCreationForm(mutable_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'signup.html', {'form': form})


@login_required
@get_organization
def dashboard_view(request, organization):
    return render(request, 'dashboard/dashboard.html', {'organization': organization,'nav_items': nav_items})

@login_required
@get_organization
def employees_list_view(request, organization):
    employees = organization.employees.all()
    return render(request, 'dashboard/employees.html', {'organization': organization,'nav_items': nav_items,'employees': employees})
    
@login_required
@get_organization
def employee_view(request, organization):
    if request.method == 'POST':
        mutable_post = request.POST.copy()
        mutable_post['username'] = request.POST['email']
        user_form = UserCreationForm(mutable_post)
        employee_form = EmployeeCreationForm(request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            color = generate_color(COLORS)
            employee = employee_form.save(commit=False)
            employee.primary_color = color['primary_color']
            employee.secondary_color = color['secondary_color']
            employee.user = user
            employee.organization = organization
            employee.save()
        
        else:
            print(user_form.errors)
            print(employee_form.errors)
        

    return redirect('employees')

@login_required
@get_organization
def schedules_view(request, organization):
    if request.method == 'POST':
        shift_form = ShiftCreationForm(request.POST)
        schedule_form = ScheduleCreationForm(request.POST)
        if shift_form.is_valid() and schedule_form.is_valid():
            shift = shift_form.save(commit=False)
            shift.organization = organization
            shift.save()
            schedule = schedule_form.save(commit=False)
            schedule.shift = shift
            schedule.organization = organization
            schedule.save()
        else:
            print(shift_form.errors)
            print(schedule_form.errors)
    current_date = datetime.now()
    start_date = current_date - timedelta(days=current_date.weekday())
    week_dates = []
    for i in range(7):
        week_dates.append(start_date + timedelta(days=i))
    return render(request, 'dashboard/schedule.html', {'organization': organization,'nav_items': nav_items, 'dates':week_dates})


@login_required
@get_organization
def create_schedule_view(request, organization):
    return render(request, 'dashboard/create_schedule.html', {'organization': organization})


@login_required
@get_organization
def shifts_delete_view(request,organization):
    if request.method == 'POST':
        pk = request.POST['shift_id']
        shift = get_object_or_404(Shift, pk=pk)
        shift.delete()
    return redirect('schedules')  # Redirect to a success URL after deletion
    