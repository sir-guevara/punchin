from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms.schedule_create_form import ShiftCreationForm, ScheduleCreationForm
from .models import Employee, Organization, Schedule, Shift
from .forms.employee_create_form import EmployeeCreationForm, UserCreationForm
from .forms.user_create_form import CustomUserCreationForm
from functools import wraps
import random,pytz
from datetime import datetime,timedelta, date
from django.utils import timezone


nav_items = [{ "name":"Dashboard", "link":"" },{ "name": "Employee","link":"employees/"},{ 
     "name":"Schedules", "link":"schedules/"}, {"name":"Time Off","link":"time-off/"},{"name":"Timesheets", "link":"timesheet"},{"name":"Reports","link":"reports"},{"name":"Messages","link":"messages/"},]


COLORS = [{'primary_color': '#F2D7D5', 'secondary_color': '#C0392B',},{'primary_color': '#FADBD8', 'secondary_color': '#E74C3C',},{'primary_color': '#EBDEF0', 'secondary_color': '#9B59B6',},{'primary_color': '#D4E6F1', 'secondary_color': '#2980B9',},{'primary_color': '#D6EAF8', 'secondary_color': '#3498DB',},{'primary_color': '#D1F2EB', 'secondary_color': '#1ABC9C',},{'primary_color': '#D0ECE7', 'secondary_color': '#16A085',},{'primary_color': '#D4EFDF', 'secondary_color': '#27AE60',},{'primary_color': '#FCF3CF', 'secondary_color': '#F1C40F',},{'primary_color': '#FDEBD0', 'secondary_color': '#F39C12',},{'primary_color': '#FAE5D3', 'secondary_color': '#E67E22',},{'primary_color': '#F6DDCC', 'secondary_color': '#D35400',},{'primary_color': '#EAEDED', 'secondary_color': '#BDC3C7',},{'primary_color': '#E5E8E8', 'secondary_color': '#7F8C8D',},{'primary_color': '#D6DBDF', 'secondary_color': '#34495E',},{'primary_color': '#D5D8DC', 'secondary_color': '#2C3E50',},]

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
            return redirect('punch_in_out')
        return view_func(request, *args, **kwargs)
    return wrapper

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('dashboard')
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
def shifts_delete_view(request):
    if request.method == 'POST':
        pk = request.POST['shift_id']
        shift = get_object_or_404(Shift, pk=pk)
        shift.delete()
    return redirect('schedules')  # Redirect to a success URL after deletion


# TODO add user shedules
@login_required
def punchin_view(request):
    user = request.user
    formatted_today = today.strftime('%Y-%m-%d')
    user_timezone = pytz.timezone(user.employee.organization.timezone)
    today = timezone.localtime(timezone.now(), timezone=user_timezone).date()


    today_schedule,future_schedule = None, None
    future_schedule= Schedule.objects.filter(employee__user=user, date__gt=today).first()

    try:
        today_schedule = get_object_or_404(Schedule,employee__user=user, date=today)
    except:
        pass    
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'staff/clock.html',{"title":"Punch In/Out","schedule":today_schedule,"next_schedule":future_schedule, "today":today})

